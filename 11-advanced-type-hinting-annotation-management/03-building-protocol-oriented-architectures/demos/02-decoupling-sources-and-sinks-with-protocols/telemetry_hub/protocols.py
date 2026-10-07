from typing import Protocol

from telemetry_hub.models import Summary


class ReadingSource(Protocol):
    def readings(self) -> list[object]: ...


class ReadingSink(Protocol):
    def write(self, summary: Summary) -> None: ...
