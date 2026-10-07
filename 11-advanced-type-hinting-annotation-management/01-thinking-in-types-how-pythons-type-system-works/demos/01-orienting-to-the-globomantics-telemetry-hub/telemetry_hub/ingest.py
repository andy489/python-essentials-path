import json
from typing import Any


class FileSource:
    def __init__(self, path: Any) -> None:
        self.path = path

    def readings(self) -> Any:
        with open(self.path, encoding="utf-8") as handle:
            return json.load(handle)
