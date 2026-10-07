from globomantics_platform.data.models import Customer
from globomantics_platform.plugins import apply_discounts


def test_plugins_apply_discounts_for_high_spender():
    customer = Customer(
        id="C999",
        name="High Roller",
        email="high@example.com",
        spend_last_12m=6000.0,
        is_active=True,
    )
    final, labels = apply_discounts(customer, amount=100.0, tier="platinum")
    assert final < 100.0
    assert "loyal-customer" in labels or "high-spender" in labels
