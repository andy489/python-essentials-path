from telemetry_hub.constraints import MaxLen, Range
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


def test_range_accepts_values_on_the_bounds():
    assert Range(-50.0, 150.0).check(150.0) is None


def test_range_reports_values_outside_the_bounds():
    assert Range(-50.0, 150.0).check(999.0) == "999.0 out of range [-50.0, 150.0]"


def test_maxlen_reports_strings_over_the_limit():
    assert MaxLen(3).check("abcd") == "length 4 exceeds max length 3"


def test_valid_payload_still_passes_with_constraints():
    assert validate_payload(Reading, make_payload()) == []


def test_out_of_range_temperature_is_a_field_level_error():
    assert validate_payload(Reading, make_payload(temperature=999.0)) == [
        "temperature: 999.0 out of range [-50.0, 150.0]"
    ]


def test_too_long_device_id_is_a_field_level_error():
    assert validate_payload(Reading, make_payload(device_id="x" * 70)) == [
        "device_id: length 70 exceeds max length 64"
    ]


def test_type_error_wins_over_constraint_checks():
    assert validate_payload(Reading, make_payload(temperature="999.0")) == [
        "temperature: expected float, got str"
    ]
