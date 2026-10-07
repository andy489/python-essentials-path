import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

from util import get_logger

logger = get_logger(__name__)


@dataclass
class Customer:
    id: str
    name: str
    email: str
    spend_last_12m: float
    is_active: bool = True


def load_customers(csv_path: str | Path) -> List[Customer]:
    path = Path(csv_path)
    logger.info(f"Loading customers from {path}")
    customers: List[Customer] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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
