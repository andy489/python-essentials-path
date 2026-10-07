from typing import Any

from telemetry_hub.models import is_valid_payload, summarize


def clean(payloads: Any) -> Any:
    return [payload for payload in payloads if is_valid_payload(payload)]


def process(payloads: Any) -> Any:
    readings = clean(payloads)
    return summarize(readings)
