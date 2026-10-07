from dataclasses import dataclass
from typing import List

from globomantics_data.models import Customer
from globomantics_analytics.tiering import compute_tier
from globomantics_plugins import apply_discounts
from globomantics_shared.logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class Invoice:
    customer_id: str
    customer_name: str
    base_amount: float
    final_amount: float
    tier: str
    discounts: list[str]


def generate_invoices(customers: List[Customer]) -> List[Invoice]:
    invoices = []
    for c in customers:
        if not c.is_active:
            continue

        base = round(c.spend_last_12m * 0.1, 2)
        tier = compute_tier(c.spend_last_12m)
        final, labels = apply_discounts(c, base, tier)

        invoices.append(
            Invoice(
                customer_id=c.id,
                customer_name=c.name,
                base_amount=base,
                final_amount=final,
                tier=tier,
                discounts=labels,
            )
        )
    return invoices
