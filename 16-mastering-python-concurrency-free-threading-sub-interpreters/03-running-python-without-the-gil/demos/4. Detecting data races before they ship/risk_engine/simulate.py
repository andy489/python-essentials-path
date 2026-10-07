import math
import random

from .portfolio import Position

HORIZON_DAYS = 30
TRADING_DAYS = 252


def _simulate_position_pnl(
    position: Position, scenarios: int, rng: random.Random
) -> list[float]:
    daily_vol = position.volatility / math.sqrt(TRADING_DAYS)
    pnls = []
    for _ in range(scenarios):
        price = position.spot
        for _ in range(HORIZON_DAYS):
            price *= 1.0 + rng.gauss(0.0, daily_vol)
        pnls.append((price - position.spot) * position.quantity)
    return pnls


def run_scenarios(
    positions: list[Position], scenarios: int, seed: int
) -> list[float]:
    rng = random.Random(seed)
    totals = [0.0] * scenarios
    for position in positions:
        for i, pnl in enumerate(_simulate_position_pnl(position, scenarios, rng)):
            totals[i] += pnl
    return totals


def summarize(pnls: list[float]) -> dict[str, float]:
    ordered = sorted(pnls)
    cutoff = max(1, len(ordered) // 20)
    tail = ordered[:cutoff]
    return {
        "var95": -ordered[cutoff - 1],
        "es95": -sum(tail) / len(tail),
        "mean": sum(pnls) / len(pnls),
    }
