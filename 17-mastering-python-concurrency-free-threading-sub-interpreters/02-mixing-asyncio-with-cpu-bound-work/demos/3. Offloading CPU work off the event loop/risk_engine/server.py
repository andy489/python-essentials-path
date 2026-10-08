import argparse
import asyncio
import json
import sys
import time
from dataclasses import replace

from .market_data import fetch_quotes
from .portfolio import demo_portfolio
from .simulate import run_scenarios, summarize

HOST = "127.0.0.1"


def run_job(scenarios: int, seed: int, quotes: dict[str, float]) -> dict[str, float]:
    positions = [
        replace(position, spot=quotes[position.symbol])
        for position in demo_portfolio()
    ]
    return summarize(run_scenarios(positions, scenarios, seed))


async def handle_simulate(job: dict) -> dict:
    scenarios = int(job.get("scenarios", 40_000))
    seed = int(job.get("seed", 7))
    symbols = [position.symbol for position in demo_portfolio()]

    io_start = time.perf_counter()
    quotes = await fetch_quotes(symbols)
    io_wall = time.perf_counter() - io_start

    cpu_start = time.perf_counter()
    report = await asyncio.to_thread(run_job, scenarios, seed, quotes)
    cpu_wall = time.perf_counter() - cpu_start

    return {
        "scenarios": scenarios,
        "seed": seed,
        "quotes": quotes,
        "var95": round(report["var95"], 2),
        "es95": round(report["es95"], 2),
        "mean": round(report["mean"], 2),
        "io_seconds": round(io_wall, 3),
        "cpu_seconds": round(cpu_wall, 3),
        "gil_enabled": sys._is_gil_enabled(),
    }


async def route(method: str, path: str, body: bytes) -> tuple[str, dict]:
    if method == "GET" and path == "/ping":
        return "200 OK", {"pong": True}
    if method == "POST" and path == "/simulate":
        try:
            job = json.loads(body) if body else {}
        except json.JSONDecodeError:
            return "400 Bad Request", {"error": "body must be valid JSON"}
        return "200 OK", await handle_simulate(job)
    return "404 Not Found", {"error": f"no route for {method} {path}"}


async def handle_connection(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
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

        status, payload = await route(method, path, body)

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


async def serve(port: int) -> None:
    server = await asyncio.start_server(handle_connection, HOST, port)
    print(f"risk engine listening on http://{HOST}:{port}", flush=True)
    async with server:
        await server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.server")
    parser.add_argument("--port", type=int, default=8123)
    args = parser.parse_args()
    asyncio.run(serve(args.port))


if __name__ == "__main__":
    main()
