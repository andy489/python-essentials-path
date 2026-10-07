import threading
import time
from concurrent import interpreters

from .portfolio import demo_portfolio
from .simulate import run_scenarios, summarize

SEED = 7
PIPELINE_JOBS = [(1_000, 7), (2_000, 8), (3_000, 9)]
AB_SCENARIOS = 50_000
AB_REPEATS = 100


def shareable_table() -> None:
    samples = [
        40_000,
        0.95,
        "var95",
        True,
        None,
        b"GLX",
        (40_000, 7, "summary"),
        [1250.0, -980.5],
        {"var95": 71_618.80},
        {"GLX"},
        demo_portfolio()[0],
    ]
    for value in samples:
        shareable = interpreters.is_shareable(value)
        print(f"  shareable={str(shareable):<6} {type(value).__name__:<9} {value!r}")


def worker_loop(jobs: interpreters.Queue, results: interpreters.Queue) -> None:
    positions = demo_portfolio()
    while True:
        job = jobs.get()
        if job is None:
            break
        job_id, scenarios, seed = job
        stats = summarize(run_scenarios(positions, scenarios, seed))
        results.put(
            (job_id, scenarios, seed, stats["var95"], stats["es95"], stats["mean"])
        )


def run_pipeline() -> None:
    interp = interpreters.create()
    jobs = interpreters.create_queue()
    results = interpreters.create_queue()
    interp.prepare_main(jobs=jobs, results=results)
    worker = threading.Thread(
        target=interp.exec,
        args=(
            "from risk_engine.boundary import worker_loop; "
            "worker_loop(jobs, results)",
        ),
    )
    worker.start()
    for job_id, (scenarios, seed) in enumerate(PIPELINE_JOBS, start=1):
        jobs.put((job_id, scenarios, seed))
    for _ in PIPELINE_JOBS:
        job_id, scenarios, seed, var95, es95, mean = results.get()
        print(
            f"  job={job_id} scenarios={scenarios:,} seed={seed} -> "
            f"var95={var95:,.2f} es95={es95:,.2f} mean={mean:,.2f}"
        )
    jobs.put(None)
    worker.join()
    interp.close()


def payload_worker(jobs: interpreters.Queue, results: interpreters.Queue) -> None:
    pnls = run_scenarios(demo_portfolio(), AB_SCENARIOS, SEED)
    stats = summarize(pnls)
    summary = (stats["var95"], stats["es95"], stats["mean"])
    results.put(("ready", len(pnls)))
    while True:
        job = jobs.get()
        if job is None:
            break
        mode, repeats = job
        payload = summary if mode == "summary" else pnls
        for _ in range(repeats):
            results.put(payload)


def measure_boundary() -> None:
    interp = interpreters.create()
    jobs = interpreters.create_queue()
    results = interpreters.create_queue()
    interp.prepare_main(jobs=jobs, results=results)
    worker = threading.Thread(
        target=interp.exec,
        args=(
            "from risk_engine.boundary import payload_worker; "
            "payload_worker(jobs, results)",
        ),
    )
    worker.start()
    _, count = results.get()
    print(
        f"  worker simulated {count:,} scenarios once; "
        f"each payload shape crosses {AB_REPEATS} times"
    )
    walls: dict[str, float] = {}
    received: dict[str, object] = {}
    for mode in ("summary", "full_list"):
        start = time.perf_counter()
        jobs.put((mode, AB_REPEATS))
        for _ in range(AB_REPEATS):
            received[mode] = results.get()
        walls[mode] = time.perf_counter() - start
        floats = 3 if mode == "summary" else count
        per_crossing = walls[mode] * 1000 / AB_REPEATS
        print(
            f"  payload={mode:<9} floats_per_crossing={floats:>6,} "
            f"wall={walls[mode]:.3f}s per_crossing={per_crossing:.2f}ms"
        )
    jobs.put(None)
    worker.join()
    interp.close()
    stats = summarize(received["full_list"])
    triple = (stats["var95"], stats["es95"], stats["mean"])
    agree = triple == received["summary"]
    print(
        f"  reduce on main matches reduce on worker: {agree} "
        f"var95={stats['var95']:,.2f}"
    )
    ratio = walls["full_list"] / walls["summary"]
    verdict = "REDUCE-ON-WORKER" if ratio >= 1.5 else "NO-CLEAR-WINNER"
    print(f"  full_list/summary={ratio:.1f}x -> verdict={verdict}")


def main() -> None:
    print("== 1. what crosses directly: interpreters.is_shareable ==")
    shareable_table()
    print()
    print("== 2. job -> result pipeline across a worker interpreter ==")
    run_pipeline()
    print()
    print("== 3. boundary cost: reduce on worker vs ship the full list ==")
    measure_boundary()


if __name__ == "__main__":
    main()
