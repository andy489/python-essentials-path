import json
from pathlib import Path

import pytest

from telemetry_hub.framework import (
    HANDLER_REGISTRY,
    TelemetryModel,
    dispatch,
    provide,
    register,
)
from telemetry_hub.gps import run_gps
from telemetry_hub.protocols import Sink


class EchoModel(TelemetryModel):
    text: str


class EchoSink:
    def __init__(self):
        self.items = []

    def write(self, item: EchoModel, /) -> None:
        self.items.append(item)


@register
def handle_echo(model: EchoModel, sink: Sink[EchoModel]) -> None:
    sink.write(model)


def test_register_uses_the_first_annotation_as_the_route_key():
    assert HANDLER_REGISTRY[EchoModel].fn is handle_echo


def test_register_records_remaining_annotations_as_dependencies():
    assert HANDLER_REGISTRY[EchoModel].dependencies == {"sink": Sink[EchoModel]}


def test_register_rejects_a_handler_without_a_model_first_parameter():
    with pytest.raises(TypeError, match="first parameter must be a TelemetryModel"):

        @register
        def bad(value: int) -> None:
            raise AssertionError("never called")


def test_dispatch_injects_the_provided_dependency():
    sink = EchoSink()
    provide(Sink[EchoModel], sink)
    model = EchoModel(text="hello")
    dispatch(model)
    assert sink.items == [model]


def test_dispatch_without_a_handler_raises_lookup_error():
    class OrphanModel(TelemetryModel):
        text: str

    with pytest.raises(LookupError, match="no handler registered for OrphanModel"):
        dispatch(OrphanModel(text="x"))


def test_dispatch_reports_a_missing_dependency():
    class LonelyModel(TelemetryModel):
        text: str

    @register
    def handle_lonely(model: LonelyModel, sink: Sink[LonelyModel]) -> None:
        sink.write(model)

    with pytest.raises(LookupError, match="no dependency provided for sink"):
        dispatch(LonelyModel(text="x"))


def test_run_gps_dispatches_valid_and_reports_invalid(tmp_path: Path, capsys):
    payloads = [
        {
            "device_id": "tracker-101",
            "latitude": 10.0,
            "longitude": 20.0,
            "timestamp": "2026-08-01T08:00:00Z",
        },
        {
            "device_id": "tracker-102",
            "latitude": 123.4,
            "longitude": 20.0,
            "timestamp": "2026-08-01T08:00:12Z",
        },
    ]
    path = tmp_path / "gps.json"
    path.write_text(json.dumps(payloads), encoding="utf-8")
    run_gps(str(path))
    out, err = capsys.readouterr()
    assert out == "gps tracker-101: lat 10.0, lon 20.0\n"
    assert "latitude: 123.4 out of range [-90.0, 90.0]" in err
