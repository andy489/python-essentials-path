from typing import Protocol

from ..data.models import Customer


class DiscountPlugin(Protocol):
    name: str

    def apply(self, customer: Customer, amount: float, tier: str) -> float:
        ...
