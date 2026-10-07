import argparse
import time
from collections.abc import Callable

from .parallel import run_processes, run_threads
from .parallel_interp import run_subinterpreters
from .portfolio import demo_portfolio
from .simulate import run_scenarios, summarize

THREAD_STEPS = [1, 2, 4, 8]
PROCESS_WORKERS = 8
INTERP_WORKERS = 8


def measure(
    mode: str, workers: int, runner: Callable[[], list[float]]
) -> dict[str, object]:
    start = time.perf_counter()
    pnls = runner()
    wall = time.perf_counter() - start
    return {
        "mode": mode,
        "workers": workers,
        "wall": wall,
        "var95": summarize(pnls)["var95"],
    }


def run_benchmark(scenarios: int, seed: int) -> list[dict[str, object]]:
    positions = demo_portfolio()
    rows = [measure("single", 1, lambda: run_scenarios(positions, scenarios, seed))]
    for workers in THREAD_STEPS:
        rows.append(
            measure(
                "threads",
                workers,
                lambda w=workers: run_threads(positions, scenarios, w, seed),
            )
        )
    rows.append(
        measure(
            "processes",
            PROCESS_WORKERS,
            lambda: run_processes(positions, scenarios, PROCESS_WORKERS, seed),
        )
    )
    rows.append(
        measure(
            "interpreters",
            INTERP_WORKERS,
            lambda: run_subinterpreters(positions, scenarios, INTERP_WORKERS, seed),
        )
    )
    return rows


def print_table(rows: list[dict[str, object]], scenarios: int, seed: int) -> None:
    baseline = rows[0]["wall"]
    print(f"benchmark scenarios={scenarios} seed={seed}")
    print(f"{'mode':<12} {'workers':>7} {'wall':>8} {'speedup':>8} {'var95':>12}")
    for row in rows:
        print(
            f"{row['mode']:<12} {row['workers']:>7} {row['wall']:>7.2f}s "
            f"{baseline / row['wall']:>7.2f}x {row['var95']:>12,.2f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.benchmark")
    parser.add_argument("--scenarios", type=int, default=40_000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    print_table(run_benchmark(args.scenarios, args.seed), args.scenarios, args.seed)


if __name__ == "__main__":
    main()
