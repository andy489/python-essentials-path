import argparse
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

BATCH_SCENARIOS = 4
BREACH_CENTS = -40_000


@dataclass(frozen=True, slots=True)
class BatchResult:
    scenarios: int
    breaches: int
    pnl_cents: int
    worst_cents: int


class RiskAggregator:
    def __init__(self) -> None:
        self.batches = 0
        self.scenarios = 0
        self.breaches = 0
        self.pnl_cents = 0
        self.worst_cents = 0

    def record(self, batch: BatchResult) -> None:
        self.batches += 1
        self.scenarios += batch.scenarios
        self.breaches += batch.breaches
        self.pnl_cents += batch.pnl_cents
        if batch.worst_cents < self.worst_cents:
            self.worst_cents = batch.worst_cents

    def merge(self, other: "RiskAggregator") -> None:
        self.batches += other.batches
        self.scenarios += other.scenarios
        self.breaches += other.breaches
        self.pnl_cents += other.pnl_cents
        if other.worst_cents < self.worst_cents:
            self.worst_cents = other.worst_cents

    def snapshot(self) -> tuple[int, int, int, int, int]:
        return (
            self.batches,
            self.scenarios,
            self.breaches,
            self.pnl_cents,
            self.worst_cents,
        )


class LockedAggregator(RiskAggregator):
    def __init__(self) -> None:
        super().__init__()
        self.lock = threading.Lock()

    def record(self, batch: BatchResult) -> None:
        with self.lock:
            super().record(batch)


def simulate_batch(rng: random.Random) -> BatchResult:
    pnls = [round(rng.gauss(0.0, 250.0) * 100) for _ in range(BATCH_SCENARIOS)]
    return BatchResult(
        scenarios=len(pnls),
        breaches=sum(1 for pnl in pnls if pnl <= BREACH_CENTS),
        pnl_cents=sum(pnls),
        worst_cents=min(pnls),
    )


def worker_batches(worker: int, batches: int, seed: int) -> list[BatchResult]:
    rng = random.Random(seed * 100_003 + worker)
    return [simulate_batch(rng) for _ in range(batches)]


def expected_totals(workers: int, batches: int, seed: int) -> RiskAggregator:
    expected = RiskAggregator()
    for worker in range(workers):
        for batch in worker_batches(worker, batches, seed):
            expected.record(batch)
    return expected


def run_shared(
    aggregator: RiskAggregator, workers: int, batches: int, seed: int
) -> RiskAggregator:
    ready = threading.Barrier(workers)

    def fold(worker: int) -> None:
        results = worker_batches(worker, batches, seed)
        ready.wait()
        for batch in results:
            aggregator.record(batch)

    threads = [
        threading.Thread(target=fold, args=(i,)) for i in range(workers)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return aggregator


def run_racy(workers: int, batches: int, seed: int) -> RiskAggregator:
    return run_shared(RiskAggregator(), workers, batches, seed)


def run_locked(workers: int, batches: int, seed: int) -> RiskAggregator:
    return run_shared(LockedAggregator(), workers, batches, seed)


def fold_partial(worker: int, batches: int, seed: int) -> RiskAggregator:
    partial = RiskAggregator()
    for batch in worker_batches(worker, batches, seed):
        partial.record(batch)
    return partial


def run_partials(workers: int, batches: int, seed: int) -> RiskAggregator:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(fold_partial, worker, batches, seed)
            for worker in range(workers)
        ]
        partials = [future.result() for future in futures]
    total = RiskAggregator()
    for partial in partials:
        total.merge(partial)
    return total


STRATEGIES = {
    "racy": run_racy,
    "locked": run_locked,
    "partials": run_partials,
}


def money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def describe(label: str, agg: RiskAggregator) -> str:
    return (
        f"{label} batches={agg.batches:,} scenarios={agg.scenarios:,} "
        f"breaches={agg.breaches:,} pnl={money(agg.pnl_cents)} "
        f"worst={money(agg.worst_cents)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.aggregator")
    parser.add_argument("--strategy", choices=list(STRATEGIES), default="racy")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--batches", type=int, default=30_000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    print(
        f"aggregator strategy={args.strategy} threads={args.threads} "
        f"batches={args.batches} seed={args.seed} "
        f"gil_enabled={sys._is_gil_enabled()}"
    )
    expected = expected_totals(args.threads, args.batches, args.seed)
    start = time.perf_counter()
    observed = STRATEGIES[args.strategy](args.threads, args.batches, args.seed)
    wall = time.perf_counter() - start
    print(describe("expected", expected))
    print(describe("observed", observed))
    lost = expected.batches - observed.batches
    lost_pct = 100.0 * lost / expected.batches
    print(f"lost={lost:,} lost_pct={lost_pct:.1f}% wall={wall:.2f}s")
    if observed.snapshot() != expected.snapshot():
        print("verdict=CORRUPTED observed totals diverged from expected")
        raise SystemExit(1)
    print("verdict=CLEAN observed totals match expected exactly")


if __name__ == "__main__":
    main()
