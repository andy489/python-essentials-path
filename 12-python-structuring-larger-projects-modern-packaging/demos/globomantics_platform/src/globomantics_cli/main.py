from globomantics_platform.config import CUSTOMERS_CSV
from globomantics_platform.logging_utils import configure_logging, get_logger
from globomantics_platform.data import load_customers
from globomantics_platform.billing import generate_invoices
from globomantics_platform.notifications import send_batch

logger = get_logger(__name__)


def main() -> None:
    configure_logging()
    customers = load_customers(CUSTOMERS_CSV)
    invoices = generate_invoices(customers)
    logger.info(f"Generated {len(invoices)} invoices")
    send_batch(invoices)


if __name__ == "__main__":
    main()
