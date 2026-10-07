import sys

from telemetry_hub.ingest import FileSource
from telemetry_hub.pipeline import process
from telemetry_hub.sinks import ConsoleSink


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "ingest":
        print("usage: python -m telemetry_hub ingest <file>")
        raise SystemExit(2)
    source = FileSource(sys.argv[2])
    summary = process(source.readings())
    sink = ConsoleSink()
    sink.write(summary)


if __name__ == "__main__":
    main()
