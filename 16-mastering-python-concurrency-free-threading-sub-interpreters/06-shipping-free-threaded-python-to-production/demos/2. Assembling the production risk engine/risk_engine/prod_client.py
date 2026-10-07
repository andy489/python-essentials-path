import argparse
import asyncio
import json
import time

from .profiling import PARALLEL_THRESHOLD

HOST = "127.0.0.1"
POLL_INTERVAL = 0.1


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
        if record["status"] == "done":
            return record
        await asyncio.sleep(POLL_INTERVAL)


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


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.prod_client")
    parser.add_argument("--port", type=int, default=8125)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--scenarios", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    asyncio.run(drive(args.port, args.jobs, args.scenarios, args.seed))


if __name__ == "__main__":
    main()
