from typing import Tuple, List

from ..data.models import Customer
from ..logging_utils import get_logger
from .base import DiscountPlugin

logger = get_logger(__name__)


class LoyalCustomerDiscount:
    name = "loyal-customer"

    def apply(self, customer: Customer, amount: float, tier: str) -> float:
        if tier in ("gold", "platinum"):
            return round(amount * 0.9, 2)
        return amount


class HighSpenderDiscount:
    name = "high-spender"

    def apply(self, customer: Customer, amount: float, tier: str) -> float:
        if customer.spend_last_12m >= 3000:
            return max(round(amount - 25.0, 2), 0.0)
        return amount


BUILTIN_PLUGINS: list[DiscountPlugin] = [
    LoyalCustomerDiscount(),
    HighSpenderDiscount(),
]


def apply_discounts(
    customer: Customer, amount: float, tier: str
) -> Tuple[float, List[str]]:
    applied: List[str] = []
    current = amount
    for plugin in BUILTIN_PLUGINS:
        new_amount = plugin.apply(customer, current, tier)
        if new_amount != current:
            applied.append(plugin.name)
            logger.info(
                f"Plugin {plugin.name} changed {customer.id} "
                f"amount from {current:.2f} to {new_amount:.2f}"
            )
            current = new_amount
    return current, applied
