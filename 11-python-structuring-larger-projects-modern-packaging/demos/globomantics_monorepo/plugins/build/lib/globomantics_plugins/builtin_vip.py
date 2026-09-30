from globomantics_shared.logging_utils import get_logger
from .base import DiscountPlugin

logger = get_logger(__name__)


class VipCustomerDiscount(DiscountPlugin):
    name = "VIP customer discount"

    def apply(self, customer, amount, tier):
        if tier == "gold" and customer.spend_last_12m > 5000:
            logger.info("Applying VIP discount for %s", customer.email)
            return amount * 0.9
        return amount