from globomantics_shared.logging_utils import get_logger
from globomantics_shared.types import Tier
from globomantics_data.models import Customer

logger = get_logger(__name__)


def compute_tier(spend_last_12m: float) -> Tier:
    if spend_last_12m >= 5000:
        return "platinum"
    if spend_last_12m >= 2000:
        return "gold"
    if spend_last_12m >= 500:
        return "silver"
    return "bronze"


def assign_tiers(customers: list[Customer]) -> dict[str, Tier]:
    logger.info("Assigning tiers")
    return {c.id: compute_tier(c.spend_last_12m) for c in customers}
