from typing import reveal_type

from telemetry_hub.models import DeviceId
from telemetry_hub.store import ReadingStore

store = ReadingStore()
device = DeviceId("sensor-001")

reveal_type(store.get_readings(device, latest=True))
