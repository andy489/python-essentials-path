import argparse
import json
import subprocess
import time
from collections.abc import Callable

from .gil_status import build_kind
from .parallel import run_threads
from .parallel_interp import run_subinterpreters
from .portfolio import Position, demo_portfolio
from .profiling import PARALLEL_THRESHOLD
from .simulate import run_scenarios, summarize

SCENARIOS = 40_000
SEED = 7
WORKERS = 8
WARMUP_SCENARIOS = 2_000
STD_LAUNCHER = "python3.14"
FT_LAUNCHER = "python3.14t"
SCALED_THRESHOLD = 1.8
TIE_BAND = 0.05
CHILD_TIMEOUT = 120

CHILD_RUNNERS: dict[str, tuple[int, Callable[[list[Position], int], list[float]]]] = {
    "single": (1, lambda positions, count: run_scenarios(positions, count, SEED)),
    "gil-threads": (
        WORKERS,
        lambda positions, count: run_threads(positions, count, WORKERS, SEED),
    ),
    "free-threads": (
        WORKERS,
        lambda positions, count: run_threads(positions, count, WORKERS, SEED),
    ),
    "interpreters": (
        WORKERS,
        lambda positions, count: run_subinterpreters(positions, count, WORKERS, SEED),
    ),
}


def run_child(strategy: str) -> None:
    workers, runner = CHILD_RUNNERS[strategy]
    positions = demo_portfolio()
    runner(positions, WARMUP_SCENARIOS)
    cpu_start = time.process_time()
    wall_start = time.perf_counter()
    pnls = runner(positions, SCENARIOS)
    wall = time.perf_counter() - wall_start
    cpu = time.process_time() - cpu_start
    print(
        json.dumps(
            {
                "strategy": strategy,
                "build": build_kind(),
                "workers": workers,
                "wall": round(wall, 3),
                "cpu": round(cpu, 3),
                "cores_used": round(cpu / wall, 1),
                "var95": round(summarize(pnls)["var95"], 2),
            }
        )
    )


def spawn_child(strategy: str, launcher: str) -> dict[str, object]:
    cmd = [
        *launcher.split(),
        "-m",
        "risk_engine.compare",
        "--child",
        strategy,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=CHILD_TIMEOUT,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"strategy": strategy, "launcher": launcher, "available": False}
    lines = result.stdout.strip().splitlines()
    if result.returncode != 0 or not lines:
        return {"strategy": strategy, "launcher": launcher, "available": False}
    row: dict[str, object] = json.loads(lines[-1])
    row["available"] = True
    return row


def run_compare(t_launcher: str) -> list[dict[str, object]]:
    rows = []
    for strategy in CHILD_RUNNERS:
        launcher = t_launcher if strategy == "free-threads" else STD_LAUNCHER
        print(f'spawn strategy={strategy} launcher="{launcher}"')
        rows.append(spawn_child(strategy, launcher))
    return rows


def tie_groups(rows: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    ranked = sorted(
        (row for row in rows if row["available"] and row["strategy"] != "single"),
        key=lambda row: row["wall"],
    )
    groups: list[list[dict[str, object]]] = []
    for row in ranked:
        if groups and row["wall"] <= groups[-1][0]["wall"] * (1 + TIE_BAND):
            groups[-1].append(row)
        else:
            groups.append([row])
    return [group for group in groups if len(group) > 1]


def print_table(rows: list[dict[str, object]]) -> None:
    baseline = rows[0]["wall"] if rows[0]["available"] else None
    print(
        f"compare scenarios={SCENARIOS} seed={SEED} workers={WORKERS} "
        f"scaled_threshold={SCALED_THRESHOLD} parallel_threshold={PARALLEL_THRESHOLD} "
        f"tie_band={TIE_BAND}"
    )
    print(
        f"{'strategy':<12} {'build':<13} {'workers':>7} {'wall':>7} {'speedup':>8} "
        f"{'throughput':>10} {'cores':>5} {'parallel':>8} {'scaled':>8} {'var95':>12}"
    )
    for row in rows:
        if not row["available"]:
            print(
                f"{row['strategy']:<12} {'unavailable':<13} {'-':>7} {'-':>7} "
                f"{'-':>8} {'-':>10} {'-':>5} {'-':>8} {'-':>8} {'-':>12}"
            )
            continue
        wall = row["wall"]
        if baseline is None:
            speedup_txt, scaled_txt = "-", "-"
        else:
            speedup = baseline / wall
            speedup_txt = f"{speedup:.2f}x"
            if row["strategy"] == "single":
                scaled_txt = "baseline"
            else:
                scaled_txt = str(speedup >= SCALED_THRESHOLD)
        parallel = row["cores_used"] >= PARALLEL_THRESHOLD
        print(
            f"{row['strategy']:<12} {row['build']:<13} {row['workers']:>7} "
            f"{wall:>6.2f}s {speedup_txt:>8} {SCENARIOS / wall:>8,.0f}/s "
            f"{row['cores_used']:>5.1f} {str(parallel):>8} {scaled_txt:>8} "
            f"{row['var95']:>12,.2f}"
        )
    for row in rows:
        if not row["available"]:
            print(
                f'note: strategy={row["strategy"]} launcher="{row["launcher"]}" '
                f"did not run; install that build to fill the row"
            )
    for group in tie_groups(rows):
        names = " and ".join(str(row["strategy"]) for row in group)
        print(
            f"note: {names} are within {TIE_BAND:.0%} wall-clock "
            f"- too close to rank on this machine"
        )


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.compare")
    parser.add_argument("--child", choices=list(CHILD_RUNNERS))
    parser.add_argument("--t-launcher", default=FT_LAUNCHER)
    args = parser.parse_args()
    if args.child:
        run_child(args.child)
    else:
        print_table(run_compare(args.t_launcher))


if __name__ == "__main__":
    main()
