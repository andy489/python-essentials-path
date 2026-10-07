import annotationlib
from annotationlib import Format
from dataclasses import dataclass


@dataclass(frozen=True)
class Sensor:
    name: str
    samples: list[float]
    zone: Zone | None


try:
    _ = Sensor.__annotations__
except NameError as error:
    print(f"__annotations__ mid-load: NameError: {error}")

try:
    annotationlib.get_annotations(Sensor, format=Format.VALUE)
except NameError as error:
    print(f"VALUE mid-load: NameError: {error}")

partial = annotationlib.get_annotations(Sensor, format=Format.FORWARDREF)
for field_name, annotation in partial.items():
    print(f"FORWARDREF mid-load: {field_name}: {annotation!r}")


@dataclass(frozen=True)
class Zone:
    name: str


resolved = annotationlib.get_annotations(Sensor, format=Format.VALUE)
print(f"VALUE after load: {resolved['zone']!r}")
