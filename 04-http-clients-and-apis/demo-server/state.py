from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

items_db = [
    {"name": "Foo", "price": 23.45},
    {"name": "Bar", "price": 67.89},
    {"name": "Baz", "price": 12.34},
    {"name": "Qux", "price": 56.78},
    {"name": "Quux", "price": 45.67},
    {"name": "Corge", "price": 78.90},
    {"name": "Grault", "price": 90.12},
    {"name": "Garply", "price": 34.56},
    {"name": "Waldo", "price": 89.01},
    {"name": "Fred", "price": 67.23},
    {"name": "Plugh", "price": 45.89},
    {"name": "Xyzzy", "price": 23.78},
    {"name": "Thud", "price": 90.23},
]

flash_messages: list[str] = []

user_id_hash: str = "0000"

_templates_dir = Path(__file__).parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(_templates_dir),
    autoescape=select_autoescape(["html"]),
)
