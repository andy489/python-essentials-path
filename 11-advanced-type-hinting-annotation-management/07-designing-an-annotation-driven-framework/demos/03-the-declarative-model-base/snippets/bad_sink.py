from telemetry_hub.protocols import ReadingSink


class MemorySink:
    def store(self, summary: object) -> None:
        print(summary)


sink: ReadingSink = MemorySink()
