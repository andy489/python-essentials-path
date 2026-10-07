from telemetry_hub.models import Reading
from telemetry_hub.validate import validate_payload


def make_payload(**overrides):
    payload = {
        "device_id": "sensor-100",
        "temperature": 20.0,
        "status": "ok",
        "timestamp": "2026-08-01T08:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_valid_payload_yields_no_errors():
    assert validate_payload(Reading, make_payload()) == []


def test_valid_optional_fields_yield_no_errors():
    payload = make_payload(
        location={"latitude": 46.05, "longitude": 14.51},
        samples=[20.5, 21.0],
    )
    assert validate_payload(Reading, payload) == []


def test_wrong_primitive_type_is_reported_per_field():
    errors = validate_payload(Reading, make_payload(temperature="21.5"))
    assert errors == ["temperature: expected float, got str"]


def test_unknown_literal_value_lists_the_allowed_values():
    errors = validate_payload(Reading, make_payload(status="boiling"))
    assert errors == [
        "status: expected one of 'ok', 'warning', 'error', got 'boiling'"
    ]


def test_nested_dataclass_error_carries_the_field_path():
    payload = make_payload(location={"latitude": "north", "longitude": 14.51})
    assert validate_payload(Reading, payload) == [
        "location.latitude: expected float, got str"
    ]


def test_union_rejects_a_value_matching_no_arm():
    errors = validate_payload(Reading, make_payload(location="garage"))
    assert errors == ["location: expected Location | None, got str"]


def test_container_elements_are_checked_by_index():
    errors = validate_payload(Reading, make_payload(samples=[20.5, "oops"]))
    assert errors == ["samples[1]: expected float, got str"]


def test_missing_required_key_is_reported():
    payload = make_payload()
    del payload["timestamp"]
    assert validate_payload(Reading, payload) == ["timestamp: missing required key"]


def test_non_dict_payload_is_rejected():
    assert validate_payload(Reading, "heartbeat") == [
        "payload: expected dict, got str"
    ]
