import sys

from telemetry_hub.ingest import FileSource
from telemetry_hub.pipeline import process
from telemetry_hub.protocols import ReadingSink, ReadingSource
from telemetry_hub.sinks import ConsoleSink, JsonLinesFileSink

USAGE = "usage: python -m telemetry_hub ingest <file> [--jsonl <path>]"


def main() -> None:
    args = sys.argv[1:]
    if len(args) not in (2, 4) or args[0] != "ingest":
        print(USAGE)
        raise SystemExit(2)
    sink: ReadingSink = ConsoleSink()
    if len(args) == 4:
        if args[2] != "--jsonl":
            print(USAGE)
            raise SystemExit(2)
        sink = JsonLinesFileSink(args[3])
    source: ReadingSource = FileSource(args[1])
    summary = process(source.readings())
    sink.write(summary)


if __name__ == "__main__":
    main()
