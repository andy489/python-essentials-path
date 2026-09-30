from dataclasses import dataclass
from typing import List

from ..data.models import Customer
from ..analytics.tiering import compute_tier
from ..plugins import apply_discounts
from ..logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class Invoice:
    customer_id: str
    customer_name: str
    base_amount: float
    final_amount: float
    tier: str
    discounts_applied: list[str]


def generate_invoices(customers: List[Customer]) -> List[Invoice]:
    invoices: List[Invoice] = []
    for c in customers:
        if not c.is_active:
            logger.info(f"Skipping inactive customer {c.id}")
            continue

        base_amount = round(c.spend_last_12m * 0.1, 2)
        tier = compute_tier(c.spend_last_12m)
        final_amount, discount_labels = apply_discounts(c, base_amount, tier)

        invoices.append(
            Invoice(
                customer_id=c.id,
                customer_name=c.name,
                base_amount=base_amount,
                final_amount=final_amount,
                tier=tier,
                discounts_applied=discount_labels,
            )
        )
    return invoices
