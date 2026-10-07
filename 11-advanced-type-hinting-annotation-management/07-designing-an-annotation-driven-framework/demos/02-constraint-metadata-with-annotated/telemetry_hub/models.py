from dataclasses import dataclass, field
from typing import Annotated, Literal, NewType, NotRequired, TypedDict, TypeIs

from telemetry_hub.constraints import MaxLen, Range

type Status = Literal["ok", "warning", "error"]

DeviceId = NewType("DeviceId", str)

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
    device_id: Annotated[DeviceId, MaxLen(64)]
    temperature: Annotated[float, Range(-50.0, 150.0)]
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
    from telemetry_hub.validate import validate_payload

    return not validate_payload(Reading, payload)


def is_known_status(value: str) -> TypeIs[Status]:
    return value in KNOWN_STATUSES


def parse_reading(payload: RawPayload) -> Reading:
    status = payload["status"]
    if not is_known_status(status):
        raise ValueError(f"unknown status: {status!r}")
    location = None
    if "location" in payload and payload["location"] is not None:
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
