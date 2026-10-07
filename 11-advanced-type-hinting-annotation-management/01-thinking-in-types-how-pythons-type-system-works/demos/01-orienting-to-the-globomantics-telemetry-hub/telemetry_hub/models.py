from typing import Any

REQUIRED_FIELDS = ("device_id", "temperature", "status", "timestamp")

KNOWN_STATUSES = ("ok", "warning", "error")


def is_valid_payload(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    return all(field in payload for field in REQUIRED_FIELDS)


def summarize(readings: Any) -> Any:
    total = len(readings)
    by_status: dict[str, int] = {}
    temperatures = []
    for reading in readings:
        status = reading["status"]
        by_status[status] = by_status.get(status, 0) + 1
        temperatures.append(reading["temperature"])
    average = sum(temperatures) / total if total else 0.0
    return {
        "total": total,
        "by_status": by_status,
        "average_temperature": round(average, 2),
    }
