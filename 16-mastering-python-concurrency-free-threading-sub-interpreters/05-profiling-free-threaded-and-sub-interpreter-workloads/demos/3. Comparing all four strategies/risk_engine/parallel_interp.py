from concurrent.futures import InterpreterPoolExecutor

from .parallel import _chunk_sizes
from .portfolio import Position
from .simulate import run_scenarios


def _interp_worker(
    positions: list[Position], count: int, seed: int
) -> list[float]:
    return run_scenarios(positions, count, seed)


def run_subinterpreters(
    positions: list[Position], scenarios: int, workers: int, seed: int
) -> list[float]:
    sizes = _chunk_sizes(scenarios, workers)
    with InterpreterPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(_interp_worker, positions, count, seed + i)
            for i, count in enumerate(sizes)
        ]
        return [pnl for future in futures for pnl in future.result()]
