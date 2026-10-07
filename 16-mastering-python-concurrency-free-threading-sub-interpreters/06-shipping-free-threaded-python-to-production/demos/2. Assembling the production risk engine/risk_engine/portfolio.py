from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    symbol: str
    quantity: int
    spot: float
    volatility: float


def demo_portfolio() -> list[Position]:
    return [
        Position("GLX", 1_200, 184.50, 0.32),
        Position("MNT", 800, 92.10, 0.45),
        Position("RSK", 2_500, 41.75, 0.28),
        Position("PLS", 600, 310.00, 0.51),
        Position("ENG", 1_500, 66.30, 0.38),
    ]
