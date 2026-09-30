from .base import DiscountPlugin
# from .builtin_loyalty import LoyalCustomerDiscount
# from .builtin_high_spender import HighSpenderDiscount
# from .builtin_vip import VipCustomerDiscount
# from .core import apply_discounts
from .core import apply_discounts, load_plugins

# __all__ = [
#     "DiscountPlugin",
#     "LoyalCustomerDiscount",
#     "HighSpenderDiscount",
#     "apply_discounts",
#     "VipCustomerDiscount"
# ]

__all__ = [
    "DiscountPlugin",
    "apply_discounts",
    "load_plugins",
]
