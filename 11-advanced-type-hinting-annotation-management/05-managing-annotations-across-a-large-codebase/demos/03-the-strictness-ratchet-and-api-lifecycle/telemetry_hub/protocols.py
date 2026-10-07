from typing import Protocol, runtime_checkable

from telemetry_hub.models import Summary


class ReadingSource(Protocol):
    def readings(self) -> list[object]: ...


@runtime_checkable
class Sink[T](Protocol):
    def write(self, item: T, /) -> None: ...


type ReadingSink = Sink[Summary]
