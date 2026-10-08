from dataclasses import dataclass

@dataclass(frozen=True)
class OrderItem:
    name: str
    itemnumber: int
    quantity: int
    price: float
    backordered: bool
