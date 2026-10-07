from dataclasses import dataclass, field
from typing import Literal, NewType, NotRequired, TypedDict, TypeIs

type Status = Literal["ok", "warning", "error"]

DeviceId = NewType("DeviceId", str)

REQUIRED_FIELDS = ("device_id", "temperature", "status", "timestamp")

KNOWN_STATUSES: tuple[Status, ...] = ("ok", "warning", "error")


class LocationPayload(TypedDict):
    latitude: float
    longitude: float


class RawPayload(TypedDict):
    device_id: str
    temperature: float
    status: str
    timestamp: str
    location: NotRequired[LocationPayload]
    samples: NotRequired[list[float]]


@dataclass(frozen=True)
class Reading:
    device_id: DeviceId
    temperature: float
    status: Status
    timestamp: str
    location: Location | None = None
    samples: list[float] = field(default_factory=list)


@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float


class Summary(TypedDict):
    total: int
    by_status: dict[Status, int]
    average_temperature: float


def is_valid_payload(payload: object) -> TypeIs[RawPayload]:
    if not isinstance(payload, dict):
        return False
    if any(key not in payload for key in REQUIRED_FIELDS):
        return False
    if "location" in payload and not isinstance(payload["location"], dict):
        return False
    if "samples" in payload and not isinstance(payload["samples"], list):
        return False
    return (
        isinstance(payload["device_id"], str)
        and type(payload["temperature"]) in (int, float)
        and isinstance(payload["status"], str)
        and isinstance(payload["timestamp"], str)
    )


def is_known_status(value: str) -> TypeIs[Status]:
    return value in KNOWN_STATUSES


def parse_reading(payload: RawPayload) -> Reading:
    status = payload["status"]
    if not is_known_status(status):
        raise ValueError(f"unknown status: {status!r}")
    location = None
    if "location" in payload:
        location = Location(
            latitude=payload["location"]["latitude"],
            longitude=payload["location"]["longitude"],
        )
    samples = list(payload["samples"]) if "samples" in payload else []
    return Reading(
        device_id=DeviceId(payload["device_id"]),
        temperature=payload["temperature"],
        status=status,
        timestamp=payload["timestamp"],
        location=location,
        samples=samples,
    )


def summarize(readings: list[Reading]) -> Summary:
    total = len(readings)
    by_status: dict[Status, int] = {}
    temperatures: list[float] = []
    for reading in readings:
        by_status[reading.status] = by_status.get(reading.status, 0) + 1
        temperatures.append(reading.temperature)
    average = sum(temperatures) / total if total else 0.0
    return {
        "total": total,
        "by_status": by_status,
        "average_temperature": round(average, 2),
    }
