import argparse
import asyncio
import json
import sys
import time
from concurrent.futures import InterpreterPoolExecutor, ThreadPoolExecutor

from .gil_status import build_kind
from .prod_worker import simulate_job

HOST = "127.0.0.1"

POOLS = {
    "threads": ThreadPoolExecutor,
    "interpreters": InterpreterPoolExecutor,
}


def log(event: str, **fields: object) -> None:
    print(json.dumps({"event": event, **fields}), flush=True)


class BusyMeter:
    def __init__(self) -> None:
        self.in_flight = 0
        self._busy_cpu = 0.0
        self._busy_wall = 0.0
        self._cpu_mark = 0.0
        self._wall_mark = 0.0

    def job_started(self) -> None:
        if self.in_flight == 0:
            self._cpu_mark = time.process_time()
            self._wall_mark = time.perf_counter()
        self.in_flight += 1

    def job_finished(self) -> None:
        self.in_flight -= 1
        if self.in_flight == 0:
            self._busy_cpu += time.process_time() - self._cpu_mark
            self._busy_wall += time.perf_counter() - self._wall_mark

    def busy_totals(self) -> tuple[float, float]:
        cpu, wall = self._busy_cpu, self._busy_wall
        if self.in_flight:
            cpu += time.process_time() - self._cpu_mark
            wall += time.perf_counter() - self._wall_mark
        return cpu, wall


class Engine:
    def __init__(self, pool: str, workers: int, queue_size: int) -> None:
        self.pool_name = pool
        self.workers = workers
        self.queue_size = queue_size
        self.queue: asyncio.Queue[int] = asyncio.Queue(maxsize=queue_size)
        self.executor = POOLS[pool](max_workers=workers)
        self.jobs: dict[int, dict] = {}
        self.meter = BusyMeter()
        self.worker_tasks: list[asyncio.Task] = []
        self.jobs_done = 0
        self.jobs_rejected = 0
        self.started = time.perf_counter()
        self._next_id = 0

    def start_workers(self) -> None:
        self.worker_tasks = [
            asyncio.create_task(self.worker_loop()) for _ in range(self.workers)
        ]

    async def worker_loop(self) -> None:
        loop = asyncio.get_running_loop()
        while True:
            job_id = await self.queue.get()
            record = self.jobs[job_id]
            record["status"] = "running"
            self.meter.job_started()
            start = time.perf_counter()
            try:
                summary = await loop.run_in_executor(
                    self.executor, simulate_job, record["scenarios"], record["seed"]
                )
            finally:
                self.meter.job_finished()
                self.queue.task_done()
            record.update(summary)
            record["wall_seconds"] = round(time.perf_counter() - start, 3)
            record["status"] = "done"
            self.jobs_done += 1
            log(
                "job_done",
                job_id=job_id,
                seed=record["seed"],
                var95=summary["var95"],
                wall_seconds=record["wall_seconds"],
                jobs_done=self.jobs_done,
            )

    def submit(self, scenarios: int, seed: int) -> tuple[str, dict]:
        if self.queue.full():
            self.jobs_rejected += 1
            log(
                "job_rejected",
                queue_depth=self.queue.qsize(),
                queue_size=self.queue_size,
                jobs_rejected=self.jobs_rejected,
            )
            return "503 Service Unavailable", {
                "error": "queue full",
                "queue_depth": self.queue.qsize(),
                "queue_size": self.queue_size,
            }
        self._next_id += 1
        job_id = self._next_id
        self.jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "scenarios": scenarios,
            "seed": seed,
            "pool": self.pool_name,
        }
        self.queue.put_nowait(job_id)
        log(
            "job_accepted",
            job_id=job_id,
            seed=seed,
            scenarios=scenarios,
            queue_depth=self.queue.qsize(),
        )
        return "202 Accepted", {
            "job_id": job_id,
            "status": "queued",
            "result": f"/result/{job_id}",
        }

    def result(self, raw_id: str) -> tuple[str, dict]:
        if not raw_id.isdigit():
            return "400 Bad Request", {"error": "job id must be an integer"}
        record = self.jobs.get(int(raw_id))
        if record is None:
            return "404 Not Found", {"error": "no such job", "job_id": int(raw_id)}
        return "200 OK", record

    def health(self) -> dict:
        return {
            "status": "ok",
            "pool": self.pool_name,
            "workers": self.workers,
            "queue_size": self.queue_size,
            "build": build_kind(),
            "gil_enabled": sys._is_gil_enabled(),
        }

    def metrics(self) -> dict:
        cpu, wall = self.meter.busy_totals()
        uptime = time.perf_counter() - self.started
        return {
            "pool": self.pool_name,
            "workers": self.workers,
            "queue_size": self.queue_size,
            "queue_depth": self.queue.qsize(),
            "in_flight": self.meter.in_flight,
            "jobs_done": self.jobs_done,
            "jobs_rejected": self.jobs_rejected,
            "throughput_busy": round(self.jobs_done / wall, 2) if wall else 0.0,
            "cores_used_busy": round(cpu / wall, 2) if wall else 0.0,
            "cores_used_lifetime": round(time.process_time() / uptime, 2),
            "uptime_seconds": round(uptime, 1),
        }

    def route(self, method: str, path: str, body: bytes) -> tuple[str, dict]:
        if method == "GET" and path == "/health":
            return "200 OK", self.health()
        if method == "GET" and path == "/metrics":
            return "200 OK", self.metrics()
        if method == "GET" and path.startswith("/result/"):
            return self.result(path.removeprefix("/result/"))
        if method == "POST" and path == "/simulate":
            try:
                job = json.loads(body) if body else {}
            except json.JSONDecodeError:
                return "400 Bad Request", {"error": "body must be valid JSON"}
            return self.submit(
                int(job.get("scenarios", 40_000)), int(job.get("seed", 7))
            )
        return "404 Not Found", {"error": f"no route for {method} {path}"}

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            request_line = await reader.readline()
            if not request_line:
                return
            method, path, _ = request_line.decode().split()
            headers: dict[str, str] = {}
            while (line := await reader.readline()) not in (b"\r\n", b"\n", b""):
                name, _, value = line.decode().partition(":")
                headers[name.strip().lower()] = value.strip()
            length = int(headers.get("content-length", "0"))
            body = await reader.readexactly(length) if length else b""

            status, payload = self.route(method, path, body)

            data = json.dumps(payload).encode()
            writer.write(
                (
                    f"HTTP/1.1 {status}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(data)}\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                ).encode()
                + data
            )
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()


async def serve(pool: str, workers: int, queue_size: int, port: int) -> None:
    engine = Engine(pool, workers, queue_size)
    engine.start_workers()
    server = await asyncio.start_server(engine.handle_connection, HOST, port)
    log(
        "ready",
        pool=pool,
        workers=workers,
        queue_size=queue_size,
        build=build_kind(),
        port=port,
        url=f"http://{HOST}:{port}",
    )
    async with server:
        await server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.production")
    parser.add_argument("--pool", choices=[*POOLS], default="interpreters")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--queue-size", type=int, default=8)
    parser.add_argument("--port", type=int, default=8125)
    args = parser.parse_args()
    asyncio.run(serve(args.pool, args.workers, args.queue_size, args.port))


if __name__ == "__main__":
    main()
