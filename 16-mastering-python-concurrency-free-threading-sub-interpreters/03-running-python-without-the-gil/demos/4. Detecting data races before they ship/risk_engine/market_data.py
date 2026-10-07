import asyncio
import time

from .portfolio import demo_portfolio

QUOTE_LATENCY = 0.3
SPOT_BUMP = 1.02

_LIVE_SPOTS = {
    position.symbol: round(position.spot * SPOT_BUMP, 2)
    for position in demo_portfolio()
}


async def fetch_quote(symbol: str) -> float:
    await asyncio.sleep(QUOTE_LATENCY)
    return _LIVE_SPOTS[symbol]


async def fetch_quotes_serial(symbols: list[str]) -> dict[str, float]:
    quotes: dict[str, float] = {}
    for symbol in symbols:
        quotes[symbol] = await fetch_quote(symbol)
    return quotes


async def fetch_quotes(symbols: list[str]) -> dict[str, float]:
    async with asyncio.TaskGroup() as tg:
        tasks = {symbol: tg.create_task(fetch_quote(symbol)) for symbol in symbols}
    return {symbol: task.result() for symbol, task in tasks.items()}


async def main() -> None:
    symbols = [position.symbol for position in demo_portfolio()]
    print(f"quote service: latency={QUOTE_LATENCY}s symbols={','.join(symbols)}")

    start = time.perf_counter()
    serial = await fetch_quotes_serial(symbols)
    serial_wall = time.perf_counter() - start

    start = time.perf_counter()
    concurrent = await fetch_quotes(symbols)
    concurrent_wall = time.perf_counter() - start

    print(f"serial      quotes={len(serial)} wall={serial_wall:.2f}s")
    print(f"concurrent  quotes={len(concurrent)} wall={concurrent_wall:.2f}s")
    print(
        f"speedup={serial_wall / concurrent_wall:.1f}x "
        f"identical={serial == concurrent}"
    )
    print(" ".join(f"{symbol}={price:.2f}" for symbol, price in concurrent.items()))


if __name__ == "__main__":
    asyncio.run(main())
