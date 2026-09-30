from globomantics_shared.logging_utils import configure_logging
from globomantics_data.loader import load_customers
from globomantics_billing.invoices import generate_invoices
from globomantics_shared.config import PROJECT_ROOT
import json


def main():
    configure_logging()

    csv = PROJECT_ROOT / "data/src/globomantics_data/samples/customers.csv"
    customers = load_customers(csv)
    invoices = generate_invoices(customers)

    print("Invoices:")
    print(json.dumps([inv.__dict__ for inv in invoices], indent=2))
