from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class Constraint(Protocol):
    def check(self, value: object) -> str | None: ...


@dataclass(frozen=True)
class Range:
    min: float
    max: float

    def check(self, value: object) -> str | None:
        if isinstance(value, (int, float)) and not self.min <= value <= self.max:
            return f"{value!r} out of range [{self.min}, {self.max}]"
        return None


@dataclass(frozen=True)
class MaxLen:
    limit: int

    def check(self, value: object) -> str | None:
        if isinstance(value, str) and len(value) > self.limit:
            return f"length {len(value)} exceeds max length {self.limit}"
        return None
