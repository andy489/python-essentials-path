import sys
from collections.abc import Callable, Iterable
from warnings import deprecated

from telemetry_hub.models import (
    RawPayload,
    Reading,
    Summary,
    is_valid_payload,
    parse_reading,
    summarize,
)
from telemetry_hub.store import ReadingStore
from telemetry_hub.validate import validate_payload

type Stage[TIn, TOut] = Callable[[TIn], TOut]


class Pipeline[TIn, TOut = TIn]:
    def __init__(self, stage: Stage[TIn, TOut]) -> None:
        self._stage = stage

    def then[TNext](self, stage: Stage[TOut, TNext]) -> Pipeline[TIn, TNext]:
        def composed(value: TIn) -> TNext:
            return stage(self._stage(value))

        return Pipeline(composed)

    def run(self, value: TIn) -> TOut:
        return self._stage(value)


def validate(payloads: Iterable[object]) -> list[RawPayload]:
    valid: list[RawPayload] = []
    for payload in payloads:
        if is_valid_payload(payload):
            valid.append(payload)
        else:
            for error in validate_payload(Reading, payload):
                print(f"invalid payload: {error}", file=sys.stderr)
    return valid


def parse(payloads: list[RawPayload]) -> list[Reading]:
    return [parse_reading(payload) for payload in payloads]


@deprecated("Use Pipeline(validate).then(parse) instead of clean()")
def clean(payloads: Iterable[object]) -> list[Reading]:
    return parse(validate(payloads))


STORE = ReadingStore()


def record(readings: list[Reading]) -> list[Reading]:
    for reading in readings:
        STORE.add(reading)
    return readings


PIPELINE: Pipeline[Iterable[object], Summary] = (
    Pipeline(validate).then(parse).then(record).then(summarize)
)


def process(payloads: Iterable[object]) -> Summary:
    return PIPELINE.run(payloads)
