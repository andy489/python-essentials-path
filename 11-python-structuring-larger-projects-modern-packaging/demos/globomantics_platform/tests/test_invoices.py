from globomantics_platform.billing import generate_invoices
from globomantics_platform.data.models import Customer


def test_generate_invoices_skips_inactive():
    customers = [
        Customer(id="C001", name="Active", email="a@example.com", spend_last_12m=1000, is_active=True),
        Customer(id="C002", name="Inactive", email="b@example.com", spend_last_12m=1000, is_active=False),
    ]
    invoices = generate_invoices(customers)
    assert len(invoices) == 1
    assert invoices[0].customer_id == "C001"
