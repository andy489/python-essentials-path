from pathlib import Path

from telemetry_hub.ingest import LegacyBatchSource
from telemetry_hub.pipeline import process


def test_legacy_batch_source_end_to_end(tmp_path: Path):
    target = tmp_path / "legacy.csv"
    target.write_text(
        "sensor-300,15.0,ok,2026-08-01T09:30:00Z\n"
        "sensor-301,60.0,error,2026-08-01T09:30:12Z\n",
        encoding="utf-8",
    )
    source = LegacyBatchSource(str(target))
    summary = process(source.readings())
    assert summary == {
        "total": 2,
        "by_status": {"ok": 1, "error": 1},
        "average_temperature": 37.5,
    }
