from collections.abc import Iterable

from telemetry_hub.models import (
    Reading,
    Summary,
    is_valid_payload,
    parse_reading,
    summarize,
)


def clean(payloads: Iterable[object]) -> list[Reading]:
    return [parse_reading(payload) for payload in payloads if is_valid_payload(payload)]


def process(payloads: Iterable[object]) -> Summary:
    readings = clean(payloads)
    return summarize(readings)
