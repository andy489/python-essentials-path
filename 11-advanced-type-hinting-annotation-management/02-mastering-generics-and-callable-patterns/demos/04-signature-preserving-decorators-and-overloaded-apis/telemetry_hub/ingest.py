import json
from typing import Any

from telemetry_hub.decorators import instrument, retry


@retry(times=3)
@instrument
def load_payloads(path: str) -> list[object]:
    with open(path, encoding="utf-8") as handle:
        payloads: list[object] = json.load(handle)
    return payloads


class FileSource:
    def __init__(self, path: Any) -> None:
        self.path = path

    def readings(self) -> Any:
        return load_payloads(self.path)
