from globomantics_data.loader import load_customers
from globomantics_billing.invoices import generate_invoices

from pathlib import Path


def test_end_to_end():
    csv = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "src"
        / "globomantics_data"
        / "samples"
        / "customers.csv"
    )
    customers = load_customers(csv)
    invoices = generate_invoices(customers)
    assert len(invoices) > 0


# WRONG (what pytest is trying)
# code/data/src/globomantics_data/samples/customers.csv

# RIGHT (where the file actually lives)
# code/globomantics_monorepo/data/src/globomantics_data/samples/customers.csv
