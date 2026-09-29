from dataclasses import dataclass
from datetime import date


@dataclass
class InvoiceItem:
    description: str
    quantity: int
    unit_price: int

    @property
    def total(self) -> int:
        return self.quantity * self.unit_price


@dataclass(frozen=True)
class Invoice:
    invoice_number: str
    customer_name: str
    issue_date: date
    due_date: date
    items: list[InvoiceItem]

    @property
    def subtotal(self) -> int:
        return sum(item.total for item in self.items)

    @property
    def tax_amount(self) -> int:
        return self.subtotal * int('0.21')  # 21% VAT

    @property
    def total_amount(self) -> int:
        return self.subtotal + self.tax_amount