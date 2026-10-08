import argparse
import cProfile
import pstats
import sys
import threading
import time
import timeit
from collections import Counter
from collections.abc import Callable

from .gil_status import build_kind
from .parallel import run_threads
from .parallel_interp import run_subinterpreters
from .portfolio import Position, demo_portfolio
from .simulate import run_scenarios

SEED = 7
TIMEIT_SCENARIOS = 2_000
TIMEIT_REPEATS = 5
PROFILE_SCENARIOS = 4_000
SAMPLE_SCENARIOS = 40_000
SAMPLE_INTERVAL = 0.001
CORES_SCENARIOS = 16_000
CORES_WORKERS = 8
PARALLEL_THRESHOLD = 1.5


class StackSampler:
    def __init__(self, target_ident: int, interval: float) -> None:
        self.target_ident = target_ident
        self.interval = interval
        self.counts: Counter[str] = Counter()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            time.sleep(self.interval)
            frame = sys._current_frames().get(self.target_ident)
            if frame is not None:
                self.counts[frame.f_code.co_name] += 1

    def __enter__(self) -> "StackSampler":
        self._thread.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self._stop.set()
        self._thread.join()


def tool_timeit(positions: list[Position]) -> None:
    print(f"tool=timeit scenarios={TIMEIT_SCENARIOS}")
    start = time.perf_counter()
    run_scenarios(positions, TIMEIT_SCENARIOS, SEED)
    single = time.perf_counter() - start
    print(f"single_reading={single:.3f}s (one cold perf_counter reading)")
    repeats = timeit.repeat(
        lambda: run_scenarios(positions, TIMEIT_SCENARIOS, SEED),
        repeat=TIMEIT_REPEATS,
        number=1,
    )
    formatted = ", ".join(f"{r:.3f}" for r in repeats)
    print(f"warm_repeats=[{formatted}]s")
    print(
        f"best_of_{TIMEIT_REPEATS}={min(repeats):.3f}s "
        f"spread={max(repeats) - min(repeats):.3f}s"
    )


def tool_cprofile(positions: list[Position]) -> None:
    print(f"tool=cprofile scenarios={PROFILE_SCENARIOS}")
    start = time.perf_counter()
    run_scenarios(positions, PROFILE_SCENARIOS, SEED)
    plain = time.perf_counter() - start
    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    run_scenarios(positions, PROFILE_SCENARIOS, SEED)
    profiler.disable()
    profiled = time.perf_counter() - start
    print(
        f"plain_wall={plain:.3f}s profiled_wall={profiled:.3f}s "
        f"overhead={profiled / plain:.1f}x"
    )
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("tottime").print_stats(5)
    rows = sorted(stats.stats.items(), key=lambda item: item[1][2], reverse=True)
    (_, _, name), (_, calls, tottime, _, _) = rows[0]
    print(f"hotspot={name} calls={calls:,} tottime={tottime:.3f}s")


def tool_sample(positions: list[Position]) -> None:
    print(
        f"tool=sample scenarios={SAMPLE_SCENARIOS} "
        f"requested_interval={SAMPLE_INTERVAL * 1000:.0f}ms"
    )
    sampler = StackSampler(threading.get_ident(), SAMPLE_INTERVAL)
    start = time.perf_counter()
    with sampler:
        run_scenarios(positions, SAMPLE_SCENARIOS, SEED)
    wall = time.perf_counter() - start
    total = sum(sampler.counts.values())
    print(f"wall={wall:.3f}s samples={total} effective_rate={total / wall:.0f}/s")
    for name, count in sampler.counts.most_common(3):
        print(f"  {name:<24} {count:>4} samples {100 * count / total:5.1f}%")


def _cores_probe(mode: str, workers: int, runner: Callable[[], object]) -> None:
    cpu_start = time.process_time()
    wall_start = time.perf_counter()
    runner()
    cpu = time.process_time() - cpu_start
    wall = time.perf_counter() - wall_start
    cores = cpu / wall
    print(
        f"mode={mode} workers={workers} cpu={cpu:.2f}s wall={wall:.2f}s "
        f"cores_used={cores:.1f} parallel={cores >= PARALLEL_THRESHOLD}"
    )


def tool_cores(positions: list[Position]) -> None:
    print(
        f"tool=cores scenarios={CORES_SCENARIOS} build={build_kind()} "
        f"threshold={PARALLEL_THRESHOLD}"
    )
    _cores_probe(
        "single", 1, lambda: run_scenarios(positions, CORES_SCENARIOS, SEED)
    )
    _cores_probe(
        "threads",
        CORES_WORKERS,
        lambda: run_threads(positions, CORES_SCENARIOS, CORES_WORKERS, SEED),
    )
    _cores_probe(
        "interpreters",
        CORES_WORKERS,
        lambda: run_subinterpreters(positions, CORES_SCENARIOS, CORES_WORKERS, SEED),
    )


TOOLS: dict[str, Callable[[list[Position]], None]] = {
    "timeit": tool_timeit,
    "cprofile": tool_cprofile,
    "sample": tool_sample,
    "cores": tool_cores,
}


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.profiling")
    parser.add_argument("--tool", choices=[*TOOLS, "all"], default="all")
    args = parser.parse_args()
    positions = demo_portfolio()
    selected = list(TOOLS) if args.tool == "all" else [args.tool]
    for index, name in enumerate(selected):
        if index:
            print()
        TOOLS[name](positions)


if __name__ == "__main__":
    main()
