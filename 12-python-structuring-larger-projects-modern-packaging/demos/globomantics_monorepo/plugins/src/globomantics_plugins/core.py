from globomantics_shared.logging_utils import get_logger
# from .builtin_loyalty import LoyalCustomerDiscount
# from .builtin_high_spender import HighSpenderDiscount
# from .builtin_vip import VipCustomerDiscount
from importlib.metadata import entry_points

logger = get_logger(__name__)

# PLUGINS = [
#     LoyalCustomerDiscount(),
#     HighSpenderDiscount(),
#     VipCustomerDiscount()
# ]

def load_plugins():
    """Discover all plugins registered via entry points."""
    eps = entry_points(group="globomantics.plugins")
    plugins = []

    for ep in eps:
        logger.info(f"Loading plugin: {ep.name}")
        plugin_cls = ep.load()
        plugins.append(plugin_cls())

    return plugins

def apply_discounts(customer, amount, tier):
    applied = []
    current = amount
    # for plugin in PLUGINS:
    for plugin in load_plugins():
        new_amount = plugin.apply(customer, current, tier)
        if new_amount != current:
            applied.append(plugin.name)
            current = new_amount
    return current, applied

