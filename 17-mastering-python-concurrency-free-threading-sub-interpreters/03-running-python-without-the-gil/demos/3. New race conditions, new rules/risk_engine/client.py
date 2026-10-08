import argparse
import asyncio
import json
import time

HOST = "127.0.0.1"


async def post_json(port: int, path: str, payload: dict) -> dict:
    reader, writer = await asyncio.open_connection(HOST, port)
    body = json.dumps(payload).encode()
    writer.write(
        (
            f"POST {path} HTTP/1.1\r\n"
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
    _, _, data = raw.partition(b"\r\n\r\n")
    return json.loads(data)


def narrate(gil_enabled: bool) -> str:
    if gil_enabled:
        return "gil=on: threaded pool serializes CPU-bound jobs; expect no scaling"
    return "gil=off: threaded pool runs CPU-bound jobs in parallel; expect scaling"


async def run_jobs(port: int, jobs: int, scenarios: int, seed: int) -> None:
    print(
        f"submitting {jobs} concurrent jobs "
        f"scenarios={scenarios} seeds={seed}..{seed + jobs - 1}"
    )
    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(
                post_json(port, "/simulate", {"scenarios": scenarios, "seed": seed + i})
            )
            for i in range(jobs)
        ]
    wall = time.perf_counter() - start

    results = [task.result() for task in tasks]
    for result in results:
        print(
            f"job seed={result['seed']} var95={result['var95']:,.2f} "
            f"io={result['io_seconds']:.2f}s cpu={result['cpu_seconds']:.2f}s "
            f"gil_enabled={result['gil_enabled']}"
        )
    print(f"total wall={wall:.2f}s throughput={jobs / wall:.2f} jobs/s")
    print(narrate(all(result["gil_enabled"] for result in results)))


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.client")
    parser.add_argument("--port", type=int, default=8123)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--scenarios", type=int, default=40_000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    asyncio.run(run_jobs(args.port, args.jobs, args.scenarios, args.seed))


if __name__ == "__main__":
    main()
