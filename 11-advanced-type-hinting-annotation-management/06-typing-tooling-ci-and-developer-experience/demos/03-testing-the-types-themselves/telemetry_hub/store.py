from typing import Literal, overload

from telemetry_hub.models import DeviceId, Reading


class ReadingStore:
    def __init__(self) -> None:
        self._by_device: dict[DeviceId, list[Reading]] = {}

    def add(self, reading: Reading) -> None:
        self._by_device.setdefault(reading.device_id, []).append(reading)

    @overload
    def get_readings(self, device_id: DeviceId) -> list[Reading]: ...

    @overload
    def get_readings(
        self, device_id: DeviceId, *, latest: Literal[True]
    ) -> Reading | None: ...

    def get_readings(
        self, device_id: DeviceId, *, latest: bool = False
    ) -> list[Reading] | Reading | None:
        readings = self._by_device.get(device_id, [])
        if latest:
            return readings[-1] if readings else None
        return list(readings)
