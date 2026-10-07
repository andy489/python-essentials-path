from typing import Literal

from customer_loader import Customer
from util import get_logger

logger = get_logger(__name__)

Tier = Literal["bronze", "silver", "gold", "platinum"]


def compute_tier(spend_last_12m: float) -> Tier:
    if spend_last_12m >= 5000:
        return "platinum"
    if spend_last_12m >= 2000:
        return "gold"
    if spend_last_12m >= 500:
        return "silver"
    return "bronze"


def assign_tiers(customers: list[Customer]) -> dict[str, Tier]:
    logger.info("Assigning tiers to customers")
    tiers: dict[str, Tier] = {}
    for c in customers:
        tiers[c.id] = compute_tier(c.spend_last_12m)
    return tiers
