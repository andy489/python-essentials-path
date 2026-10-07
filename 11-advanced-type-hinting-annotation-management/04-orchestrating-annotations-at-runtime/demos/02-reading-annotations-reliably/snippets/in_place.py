from typing import assert_type

from telemetry_hub.models import Reading
from telemetry_hub.pipeline import Pipeline


def drop_errors(readings: list[Reading]) -> list[Reading]:
    return [reading for reading in readings if reading.status != "error"]


in_place: Pipeline[list[Reading]] = Pipeline(drop_errors)
assert_type(in_place.run([]), list[Reading])
