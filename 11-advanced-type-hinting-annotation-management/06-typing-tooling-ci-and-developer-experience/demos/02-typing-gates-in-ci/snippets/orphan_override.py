from typing import override

from telemetry_hub.models import Summary
from telemetry_hub.sinks import JsonLinesFileSink


class ArchivingJsonLinesSink(JsonLinesFileSink):
    @override
    def write_line(self, summary: Summary) -> None:
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(f"total={summary['total']}\n")
