import annotationlib
from annotationlib import Format

from telemetry_hub.models import Reading


def annotations_of(cls: type, format: Format) -> dict[str, object]:
    return annotationlib.get_annotations(cls, format=format)


def main() -> None:
    for fmt in (Format.VALUE, Format.FORWARDREF, Format.STRING):
        print(f"--- {fmt.name} ---")
        for name, annotation in annotations_of(Reading, fmt).items():
            print(f"{name}: {annotation!r}")


if __name__ == "__main__":
    main()
