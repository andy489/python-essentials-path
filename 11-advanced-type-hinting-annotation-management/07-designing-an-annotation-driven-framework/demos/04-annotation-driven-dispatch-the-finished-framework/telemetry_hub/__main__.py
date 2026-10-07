import sys

from telemetry_hub.gps import run_gps
from telemetry_hub.ingest import FileSource, LegacyBatchSource
from telemetry_hub.models import Summary
from telemetry_hub.pipeline import process
from telemetry_hub.protocols import ReadingSource, Sink
from telemetry_hub.sinks import ConsoleSink, JsonLinesFileSink

USAGE = (
    "usage: python -m telemetry_hub ingest <file> [--jsonl <path>] [--legacy]"
    " | gps <file>"
)


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "gps":
        run_gps(args[1])
        return
    if len(args) not in (2, 3, 4) or args[0] != "ingest":
        print(USAGE)
        raise SystemExit(2)
    sink: Sink[Summary] = ConsoleSink()
    legacy = False
    if len(args) == 3:
        if args[2] != "--legacy":
            print(USAGE)
            raise SystemExit(2)
        legacy = True
    elif len(args) == 4:
        if args[2] != "--jsonl":
            print(USAGE)
            raise SystemExit(2)
        sink = JsonLinesFileSink(args[3])
    source: ReadingSource = LegacyBatchSource(args[1]) if legacy else FileSource(args[1])
    summary = process(source.readings())
    sink.write(summary)


if __name__ == "__main__":
    main()
