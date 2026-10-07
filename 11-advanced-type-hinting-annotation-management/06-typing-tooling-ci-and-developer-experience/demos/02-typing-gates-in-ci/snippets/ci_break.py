from telemetry_hub.models import DeviceId
from telemetry_hub.store import ReadingStore


def latest_temperature(store: ReadingStore, device_id: str) -> float:
    reading = store.get_readings(DeviceId(device_id), latest=True)
    return reading.temperature
