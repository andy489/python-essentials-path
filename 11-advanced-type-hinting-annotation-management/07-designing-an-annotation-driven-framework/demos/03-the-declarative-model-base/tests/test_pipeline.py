import pytest

from telemetry_hub.models import DeviceId, Location, Reading
from telemetry_hub.pipeline import Pipeline, clean, parse, process, validate


def make_payload(**overrides):
    payload = {
        "device_id": "sensor-100",
        "temperature": 20.0,
        "status": "ok",
        "timestamp": "2026-08-01T08:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_clean_stages_drop_incomplete_payloads():
    payloads = [make_payload(), {"note": "heartbeat"}]
    assert Pipeline(validate).then(parse).run(payloads) == [
        Reading(
            device_id=DeviceId("sensor-100"),
            temperature=20.0,
            status="ok",
            timestamp="2026-08-01T08:00:00Z",
        )
    ]


def test_clean_stages_parse_optional_location_and_samples():
    payloads = [
        make_payload(
            location={"latitude": 46.05, "longitude": 14.51},
            samples=[20.5, 21.0],
        )
    ]
    [reading] = Pipeline(validate).then(parse).run(payloads)
    assert reading.location == Location(latitude=46.05, longitude=14.51)
    assert reading.samples == [20.5, 21.0]


def test_clean_stages_drop_malformed_location():
    payloads = [make_payload(location="garage")]
    assert Pipeline(validate).then(parse).run(payloads) == []


def test_clean_stages_drop_string_temperature():
    payloads = [make_payload(temperature="21.5")]
    assert Pipeline(validate).then(parse).run(payloads) == []


def test_clean_is_deprecated_but_still_works():
    with pytest.warns(DeprecationWarning, match="Use Pipeline"):
        readings = clean([make_payload()])
    assert [reading.device_id for reading in readings] == [DeviceId("sensor-100")]


def test_process_summarizes_readings():
    payloads = [
        make_payload(temperature=10.0, status="ok"),
        make_payload(temperature=30.0, status="error"),
    ]
    summary = process(payloads)
    assert summary["total"] == 2
    assert summary["by_status"] == {"ok": 1, "error": 1}
    assert summary["average_temperature"] == 20.0


def test_process_handles_empty_input():
    summary = process([])
    assert summary["total"] == 0
    assert summary["average_temperature"] == 0.0
