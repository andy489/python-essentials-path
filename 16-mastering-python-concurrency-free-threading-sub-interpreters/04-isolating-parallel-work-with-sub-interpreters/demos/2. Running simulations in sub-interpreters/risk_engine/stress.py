import argparse
import faulthandler
import sys
import threading
import time

from .aggregator import (
    BATCH_SCENARIOS,
    STRATEGIES,
    RiskAggregator,
    expected_totals,
)


def check_invariants(
    observed: RiskAggregator, expected: RiskAggregator
) -> list[str]:
    broken = []
    if observed.snapshot() != expected.snapshot():
        broken.append("exact-totals")
    if observed.scenarios != observed.batches * BATCH_SCENARIOS:
        broken.append("scenarios-per-batch")
    if observed.breaches > observed.scenarios:
        broken.append("breach-bound")
    return broken


def run_trials(
    strategy: str,
    trials: int,
    threads: int,
    batches: int,
    seed: int,
    fail_fast: bool,
    expected: RiskAggregator,
) -> tuple[int, int]:
    completed = 0
    failed = 0
    for trial in range(1, trials + 1):
        start = time.perf_counter()
        observed = STRATEGIES[strategy](threads, batches, seed)
        wall = time.perf_counter() - start
        completed = trial
        broken = check_invariants(observed, expected)
        if broken:
            failed += 1
            lost = expected.batches - observed.batches
            print(
                f"trial {trial}/{trials} FAIL lost={lost:,} "
                f"broke={','.join(broken)} wall={wall:.2f}s"
            )
            if fail_fast:
                print("fail-fast: stopping at the first corrupted trial")
                break
        else:
            print(f"trial {trial}/{trials} PASS lost=0 wall={wall:.2f}s")
    return completed, failed


def verdict(trials: int, completed: int, failed: int, fail_fast: bool) -> str:
    if failed == 0:
        return f"verdict=ALL-CLEAN no corruption in {completed} trials"
    if fail_fast and completed < trials:
        return (
            f"verdict=CORRUPTED stopped at trial {completed} of {trials} "
            f"(fail-fast)"
        )
    if failed == completed:
        return f"verdict=PERSISTENT all {completed} trials corrupted"
    return f"verdict=INTERMITTENT {failed} of {completed} trials corrupted"


def _wait_for_lock(lock: threading.Lock) -> None:
    lock.acquire()


def demo_hang() -> None:
    held = threading.Lock()
    held.acquire()
    worker = threading.Thread(
        target=_wait_for_lock, args=(held,), name="stuck-folder"
    )
    print("demo-hang: 'stuck-folder' waits on a lock the main thread holds")
    worker.start()
    faulthandler.dump_traceback_later(1.0)
    worker.join(3.0)
    faulthandler.cancel_dump_traceback_later()
    held.release()
    worker.join()
    print("demo-hang: stacks dumped while hung, lock released, exiting cleanly")


def main() -> None:
    parser = argparse.ArgumentParser(prog="risk_engine.stress")
    parser.add_argument("--strategy", choices=list(STRATEGIES), default="racy")
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--batches", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--watchdog", type=float, default=120.0)
    parser.add_argument("--demo-hang", action="store_true")
    args = parser.parse_args()

    faulthandler.enable()
    if args.demo_hang:
        demo_hang()
        return

    print(
        f"stress strategy={args.strategy} threads={args.threads} "
        f"batches={args.batches} trials={args.trials} seed={args.seed} "
        f"fail_fast={args.fail_fast} gil_enabled={sys._is_gil_enabled()}"
    )
    expected = expected_totals(args.threads, args.batches, args.seed)
    faulthandler.dump_traceback_later(args.watchdog, exit=True)
    completed, failed = run_trials(
        args.strategy,
        args.trials,
        args.threads,
        args.batches,
        args.seed,
        args.fail_fast,
        expected,
    )
    faulthandler.cancel_dump_traceback_later()
    print(f"summary trials={completed} failed={failed}")
    print(verdict(args.trials, completed, failed, args.fail_fast))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
