from telemetry_hub.models import Summary
from telemetry_hub.protocols import Sink


class BadSummarySink:
    def write(self, summary: str) -> None:
        print(summary.upper())


def main() -> None:
    bad = BadSummarySink()
    print(f"isinstance says sink: {isinstance(bad, Sink)}")
    summary: Summary = {
        "total": 1,
        "by_status": {"ok": 1},
        "average_temperature": 21.5,
    }
    sink: Sink[Summary] = bad
    sink.write(summary)


if __name__ == "__main__":
    main()
