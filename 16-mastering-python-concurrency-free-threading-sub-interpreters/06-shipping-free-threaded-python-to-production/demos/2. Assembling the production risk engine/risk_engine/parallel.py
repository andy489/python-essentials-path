import threading
from concurrent.futures import ProcessPoolExecutor

from .portfolio import Position
from .simulate import run_scenarios


def _chunk_sizes(total: int, workers: int) -> list[int]:
    base, extra = divmod(total, workers)
    return [base + (1 if i < extra else 0) for i in range(workers)]


def run_threads(
    positions: list[Position], scenarios: int, workers: int, seed: int
) -> list[float]:
    sizes = _chunk_sizes(scenarios, workers)
    results: list[list[float]] = [[] for _ in sizes]

    def worker(index: int, count: int) -> None:
        results[index] = run_scenarios(positions, count, seed + index)

    threads = [
        threading.Thread(target=worker, args=(i, count))
        for i, count in enumerate(sizes)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return [pnl for chunk in results for pnl in chunk]

def run_processes(
    positions: list[Position], scenarios: int, workers: int, seed: int
) -> list[float]:
    sizes = _chunk_sizes(scenarios, workers)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(run_scenarios, positions, count, seed + i)
            for i, count in enumerate(sizes)
        ]
        return [pnl for future in futures for pnl in future.result()]
