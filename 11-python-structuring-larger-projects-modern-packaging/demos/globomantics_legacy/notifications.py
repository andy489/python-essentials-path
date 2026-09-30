from billing import Invoice
from util import get_logger

logger = get_logger(__name__)


def send_invoice_email(invoice: Invoice) -> None:
    # In reality this would integrate with an email provider.
    logger.info(
        f"Email to {invoice.customer_name} "
        f"(tier={invoice.tier}): amount={invoice.final_amount:.2f} "
        f"discounts={invoice.discounts_applied}"
    )


def send_batch(invoices: list[Invoice]) -> None:
    for inv in invoices:
        send_invoice_email(inv)
