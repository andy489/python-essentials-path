from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
