from telemetry_hub.pipeline import clean, process
from telemetry_hub.models import DeviceId, Reading


def make_payload(**overrides):
    payload = {
        "device_id": "sensor-100",
        "temperature": 20.0,
        "status": "ok",
        "timestamp": "2026-08-01T08:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_clean_drops_incomplete_payloads():
    payloads = [make_payload(), {"note": "heartbeat"}]
    assert clean(payloads) == [
        Reading(
            device_id=DeviceId("sensor-100"),
            temperature=20.0,
            status="ok",
            timestamp="2026-08-01T08:00:00Z",
        )
    ]

def test_clean_drops_string_temperature():
    payloads = [make_payload(temperature="21.5")]
    assert clean(payloads) == []

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
