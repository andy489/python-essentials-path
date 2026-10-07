import json

from telemetry_hub.models import Summary


class ConsoleSink:
    def write(self, summary: Summary) -> None:
        print(f"readings: {summary['total']}")
        for status, count in sorted(summary["by_status"].items()):
            print(f"  {status}: {count}")
        print(f"average temperature: {summary['average_temperature']}")


class JsonLinesFileSink:
    def __init__(self, path: str) -> None:
        self.path = path

    def write(self, summary: Summary) -> None:
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(summary, sort_keys=True) + "\n")
