from collections.abc import Iterable
from typing import assert_type

from telemetry_hub.ingest import load_payloads
from telemetry_hub.models import DeviceId, Reading, Summary
from telemetry_hub.pipeline import PIPELINE, Pipeline, parse, validate
from telemetry_hub.store import ReadingStore


def check_get_readings_all(store: ReadingStore, device: DeviceId) -> None:
    assert_type(store.get_readings(device), list[Reading])


def check_get_readings_latest(store: ReadingStore, device: DeviceId) -> None:
    assert_type(store.get_readings(device, latest=True), Reading | None)


def check_pipeline_composition() -> None:
    composed = Pipeline(validate).then(parse)
    assert_type(composed, Pipeline[Iterable[object], list[Reading]])


def check_pipeline_run(payloads: Iterable[object]) -> None:
    assert_type(PIPELINE.run(payloads), Summary)


def check_decorated_signature(path: str) -> None:
    assert_type(load_payloads(path), list[object])
