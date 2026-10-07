from typing import assert_type

from telemetry_hub.models import DeviceId, Reading
from telemetry_hub.store import ReadingStore

store = ReadingStore()
device = DeviceId("sensor-001")

assert_type(store.get_readings(device), Reading | None)
