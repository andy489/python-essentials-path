from telemetry_hub.framework import TelemetryModel


class PingModel(TelemetryModel):
    device: str
    count: int


PingModel(device=123, count=1)
PingModel(device="gateway-1")
