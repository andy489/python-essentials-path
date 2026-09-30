from dataclasses import dataclass


@dataclass
class Customer:
    id: str
    name: str
    email: str
    spend_last_12m: float
    is_active: bool = True
