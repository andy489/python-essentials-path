import pytest

from telemetry_hub.decorators import instrument, retry


def test_retry_returns_after_transient_failures():
    calls = []

    @retry(times=3)
    def flaky() -> str:
        calls.append("call")
        if len(calls) < 3:
            raise RuntimeError("transient")
        return "ok"

    assert flaky() == "ok"
    assert len(calls) == 3


def test_retry_reraises_after_all_attempts():
    @retry(times=2)
    def always_fails() -> None:
        raise RuntimeError("permanent")

    with pytest.raises(RuntimeError, match="permanent"):
        always_fails()


def test_instrument_preserves_result_and_metadata():
    @instrument
    def double(value: int) -> int:
        return value * 2

    assert double(21) == 42
    assert double.__name__ == "double"
