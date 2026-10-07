import argparse
import asyncio
import json
import time

from .profiling import PARALLEL_THRESHOLD

HOST = "127.0.0.1"
POLL_INTERVAL = 0.1
TERMINAL = {"done", "failed", "timeout"}


async def request(
    port: int, method: str, path: str, payload: dict | None = None
) -> tuple[int, dict]:
    reader, writer = await asyncio.open_connection(HOST, port)
    body = json.dumps(payload).encode() if payload is not None else b""
    writer.write(
        (
            f"{method} {path} HTTP/1.1\r\n"
            f"Host: {HOST}:{port}\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode()
        + body
    )
    await writer.drain()
    raw = await reader.read()
    writer.close()
    await writer.wait_closed()
    head, _, data = raw.partition(b"\r\n\r\n")
    return int(head.split()[1]), json.loads(data)


async def poll_result(port: int, job_id: int) -> dict:
    while True:
        _, record = await request(port, "GET", f"/result/{job_id}")
        if record["status"] in TERMINAL:
            return record
        await asyncio.sleep(POLL_INTERVAL)


async def submit(port: int, scenarios: int, seed: int, fault: str = "") -> tuple[int, dict]:
    payload = {"scenarios": scenarios, "seed": seed}
    if fault:
        payload["fault"] = fault
    return await request(port, "POST", "/simulate", payload)


async def drive(port: int, jobs: int, scenarios: int, seed: int) -> None:
    _, health = await request(port, "GET", "/health")
    print(
        f"health status={health['status']} pool={health['pool']} "
        f"build={health['build']} workers={health['workers']} "
        f"queue_size={health['queue_size']}"
    )

    print(
        f"submitting {jobs} jobs scenarios={scenarios} "
        f"seeds={seed}..{seed + jobs - 1}"
    )
    accepted: list[int] = []
    rejected = 0
    for i in range(jobs):
        status, payload = await request(
            port, "POST", "/simulate", {"scenarios": scenarios, "seed": seed + i}
        )
        if status == 202:
            accepted.append(payload["job_id"])
        else:
            rejected += 1
    verdict = "OBSERVED" if rejected else "NONE"
    print(f"accepted={len(accepted)} rejected_503={rejected} backpressure={verdict}")

    start = time.perf_counter()
    records = [await poll_result(port, job_id) for job_id in accepted]
    poll_wall = time.perf_counter() - start
    for record in records:
        print(
            f"job id={record['job_id']} seed={record['seed']} "
            f"status={record['status']} var95={record['var95']:,.2f} "
            f"pool={record['pool']}"
        )
    done = sum(1 for record in records if record["status"] == "done")
    print(f"completed={done}/{len(accepted)} poll_wall={poll_wall:.2f}s")

    _, m = await request(port, "GET", "/metrics")
    print(
        f"metrics jobs_done={m['jobs_done']} jobs_rejected={m['jobs_rejected']} "
        f"queue_depth={m['queue_depth']} in_flight={m['in_flight']} "
        f"throughput_busy={m['throughput_busy']:.2f} jobs/s"
    )
    busy, lifetime = m["cores_used_busy"], m["cores_used_lifetime"]
    print(
        f"cores busy={busy:.2f} lifetime={lifetime:.2f} "
        f"parallel_while_busy={busy >= PARALLEL_THRESHOLD} "
        f"lifetime_underreports={lifetime < busy}"
    )


async def break_then_drain(port: int, scenarios: int, seed: int) -> None:
    _, health = await request(port, "GET", "/health")
    print(
        f"health status={health['status']} pool={health['pool']} "
        f"build={health['build']} job_timeout={health['job_timeout']}s"
    )

    ids: dict[str, int] = {}
    plan = [
        ("good-1", "", seed),
        ("good-2", "", seed + 1),
        ("crash", "crash", seed + 2),
        ("hang", "hang", seed + 3),
    ]
    for label, fault, job_seed in plan:
        _, payload = await submit(port, scenarios, job_seed, fault)
        ids[label] = payload["job_id"]
    print(f"submitted good=2 crash=1 hang=1 ids={sorted(ids.values())}")

    crash = await poll_result(port, ids["crash"])
    print(
        f"job id={crash['job_id']} fault=crash status={crash['status']} "
        f"error_type={crash['error_type']} cause={crash['error_cause']} "
        f"error={crash['error']!r}"
    )

    hang = await poll_result(port, ids["hang"])
    _, m = await request(port, "GET", "/metrics")
    stuck = m["pool_slots_stuck"]
    print(
        f"job id={hang['job_id']} fault=hang status={hang['status']} "
        f"timeout_seconds={hang['timeout_seconds']}"
    )
    print(
        f"timeout_returned_before_worker_finished={stuck >= 1} "
        f"pool_slots_stuck={stuck}"
    )

    _, health = await request(port, "GET", "/health")
    print(f"health_during_faults={health['status']}")

    for label in ("good-1", "good-2"):
        record = await poll_result(port, ids[label])
        print(
            f"job id={record['job_id']} seed={record['seed']} "
            f"status={record['status']} var95={record['var95']:,.2f}"
        )

    while True:
        _, m = await request(port, "GET", "/metrics")
        if m["pool_slots_stuck"] == 0:
            break
        await asyncio.sleep(POLL_INTERVAL)
    print(f"stuck_slot_released=True in_flight={m['in_flight']}")

    for job_seed in (seed + 4, seed + 5):
        await submit(port, scenarios, job_seed)
    shutdown = asyncio.ensure_future(request(port, "POST", "/shutdown"))
    while True:
        _, health = await request(port, "GET", "/health")
        if health["draining"]:
            break
        await asyncio.sleep(0.05)
    print(f"draining=True health={health['status']}")

    status, refusal = await submit(port, scenarios, seed + 6)
    print(f"post_drain_submit={status} marker={refusal['error']}")

    _, report = await shutdown
    clean = (
        "clean"
        if report["status"] == "drained" and report["accepted_lost"] == 0
        else "dirty"
    )
    print(
        f"drained={clean} accepted_lost={report['accepted_lost']} "
        f"jobs_done={report['jobs_done']} jobs_failed={report['jobs_failed']} "
        f"jobs_timeout={report['jobs_timeout']}"
    )

    for _ in range(100):
        try:
            await request(port, "GET", "/health")
        except (OSError, IndexError):
            print("listener_closed=True")
            return
        await asyncio.sleep(0.05)
    print("listener_closed=False")


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.prod_client")
    parser.add_argument("--port", type=int, default=8125)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--scenarios", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--scenario", choices=["burst", "break-then-drain"], default="burst"
    )
    args = parser.parse_args()
    if args.scenario == "burst":
        asyncio.run(drive(args.port, args.jobs, args.scenarios, args.seed))
    else:
        asyncio.run(break_then_drain(args.port, args.scenarios, args.seed))


if __name__ == "__main__":
    main()
