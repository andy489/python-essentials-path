import sys
from typing import Annotated, TypedDict, TypeIs

from telemetry_hub.constraints import MaxLen, Range
from telemetry_hub.framework import TelemetryModel, dispatch, provide, register
from telemetry_hub.ingest import load_payloads
from telemetry_hub.models import DeviceId
from telemetry_hub.protocols import Sink
from telemetry_hub.validate import validate_payload


class GpsReading(TelemetryModel, frozen=True):
    device_id: Annotated[DeviceId, MaxLen(64)]
    latitude: Annotated[float, Range(-90.0, 90.0)]
    longitude: Annotated[float, Range(-180.0, 180.0)]
    timestamp: str


class GpsPayload(TypedDict):
    device_id: str
    latitude: float
    longitude: float
    timestamp: str


class GpsConsoleSink:
    def write(self, reading: GpsReading, /) -> None:
        print(
            f"gps {reading.device_id}: "
            f"lat {reading.latitude}, lon {reading.longitude}"
        )


@register
def handle(reading: GpsReading, sink: Sink[GpsReading]) -> None:
    sink.write(reading)


def is_valid_gps(payload: object) -> TypeIs[GpsPayload]:
    return not validate_payload(GpsReading, payload)


def parse_gps(payload: GpsPayload) -> GpsReading:
    return GpsReading(
        device_id=DeviceId(payload["device_id"]),
        latitude=payload["latitude"],
        longitude=payload["longitude"],
        timestamp=payload["timestamp"],
    )


def run_gps(path: str) -> None:
    sink: Sink[GpsReading] = GpsConsoleSink()
    provide(Sink[GpsReading], sink)
    for payload in load_payloads(path):
        if is_valid_gps(payload):
            dispatch(parse_gps(payload))
        else:
            for error in validate_payload(GpsReading, payload):
                print(f"invalid payload: {error}", file=sys.stderr)
