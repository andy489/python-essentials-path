import json
from pathlib import Path

from telemetry_hub.models import Summary
from telemetry_hub.sinks import JsonLinesFileSink, RotatingJsonLinesSink


def make_summary(total: int, average: float) -> Summary:
    return {
        "total": total,
        "by_status": {"ok": total},
        "average_temperature": average,
    }


def test_jsonl_sink_writes_summary_as_one_sorted_json_line(tmp_path: Path):
    target = tmp_path / "summaries.jsonl"
    sink = JsonLinesFileSink(str(target))
    sink.write(make_summary(2, 20.65))
    lines = target.read_text(encoding="utf-8").splitlines()
    assert lines == [
        '{"average_temperature": 20.65, "by_status": {"ok": 2}, "total": 2}'
    ]


def test_jsonl_sink_appends_across_writes(tmp_path: Path):
    target = tmp_path / "summaries.jsonl"
    sink = JsonLinesFileSink(str(target))
    sink.write(make_summary(2, 20.65))
    sink.write(make_summary(3, 30.0))
    written = [
        json.loads(line)
        for line in target.read_text(encoding="utf-8").splitlines()
    ]
    assert written == [make_summary(2, 20.65), make_summary(3, 30.0)]


def test_rotating_sink_moves_full_file_aside_before_writing(tmp_path: Path):
    target = tmp_path / "summaries.jsonl"
    sink = RotatingJsonLinesSink(str(target), max_lines=2)
    for total in (1, 2, 3):
        sink.write(make_summary(total, 20.0))
    current = target.read_text(encoding="utf-8").splitlines()
    rotated = (tmp_path / "summaries.jsonl.1").read_text(encoding="utf-8").splitlines()
    assert [json.loads(line)["total"] for line in current] == [3]
    assert [json.loads(line)["total"] for line in rotated] == [1, 2]


def test_rotating_sink_below_the_limit_never_rotates(tmp_path: Path):
    target = tmp_path / "summaries.jsonl"
    sink = RotatingJsonLinesSink(str(target), max_lines=2)
    sink.write(make_summary(1, 20.0))
    sink.write(make_summary(2, 21.0))
    assert not (tmp_path / "summaries.jsonl.1").exists()
    assert len(target.read_text(encoding="utf-8").splitlines()) == 2
