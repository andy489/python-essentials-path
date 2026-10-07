from pathlib import Path

from customer_loader import load_customers
from billing import generate_invoices
from notifications import send_batch
from util import get_logger

logger = get_logger(__name__)


def main() -> None:
    data_path = Path("data") / "customers_sample.csv"
    customers = load_customers(data_path)
    invoices = generate_invoices(customers)
    logger.info(f"Generated {len(invoices)} invoices")
    send_batch(invoices)


if __name__ == "__main__":
    main()
