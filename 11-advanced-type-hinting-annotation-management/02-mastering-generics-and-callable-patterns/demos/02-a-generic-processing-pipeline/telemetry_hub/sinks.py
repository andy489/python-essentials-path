from typing import Any


class ConsoleSink:
    def write(self, summary: Any) -> None:
        print(f"readings: {summary['total']}")
        for status, count in sorted(summary["by_status"].items()):
            print(f"  {status}: {count}")
        print(f"average temperature: {summary['average_temperature']}")
