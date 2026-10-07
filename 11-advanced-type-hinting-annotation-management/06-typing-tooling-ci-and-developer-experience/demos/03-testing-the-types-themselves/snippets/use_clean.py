from telemetry_hub.models import Reading
from telemetry_hub.pipeline import clean


def ingest_batch(payloads: list[object]) -> list[Reading]:
    return clean(payloads)
