from telemetry_hub.models import DeviceId, Reading
from telemetry_hub.store import ReadingStore


def make_reading(device_id: str, temperature: float, timestamp: str) -> Reading:
    return Reading(
        device_id=DeviceId(device_id),
        temperature=temperature,
        status="ok",
        timestamp=timestamp,
    )


def test_get_readings_returns_every_reading_for_a_device():
    store = ReadingStore()
    first = make_reading("sensor-001", 20.0, "2026-08-01T08:00:00Z")
    second = make_reading("sensor-001", 21.0, "2026-08-01T08:01:00Z")
    store.add(first)
    store.add(second)
    store.add(make_reading("sensor-002", 47.9, "2026-08-01T08:00:12Z"))
    assert store.get_readings(DeviceId("sensor-001")) == [first, second]


def test_get_readings_latest_returns_the_newest_reading():
    store = ReadingStore()
    store.add(make_reading("sensor-001", 20.0, "2026-08-01T08:00:00Z"))
    newest = make_reading("sensor-001", 88.2, "2026-08-01T08:01:00Z")
    store.add(newest)
    assert store.get_readings(DeviceId("sensor-001"), latest=True) == newest


def test_get_readings_unknown_device_returns_empty_list():
    store = ReadingStore()
    assert store.get_readings(DeviceId("sensor-404")) == []


def test_get_readings_latest_unknown_device_returns_none():
    store = ReadingStore()
    assert store.get_readings(DeviceId("sensor-404"), latest=True) is None
