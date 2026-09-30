import csv
from pathlib import Path
from globomantics_shared.logging_utils import get_logger

from typing import List
from .models import Customer

logger = get_logger(__name__)


def load_customers(csv_path: Path) -> List[Customer]:
    customers = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            from .models import Customer  # local import for monorepo clarity
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
