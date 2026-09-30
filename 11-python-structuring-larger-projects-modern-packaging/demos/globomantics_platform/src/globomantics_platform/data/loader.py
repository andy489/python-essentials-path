import csv
from pathlib import Path
from typing import Iterable, List

from .models import Customer
from ..logging_utils import get_logger

logger = get_logger(__name__)


def load_customers(path: Path | str) -> List[Customer]:
    csv_path = Path(path)
    logger.info(f"Loading customers from {csv_path}")
    customers: List[Customer] = []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader: Iterable[dict[str, str]] = csv.DictReader(f)
        for row in reader:
            customers.append(
                Customer(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    spend_last_12m=float(row["spend_last_12m"]),
                    is_active=row["is_active"].lower() == "true",
                )
            )
    return customers
