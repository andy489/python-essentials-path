# Worker functions used by notebook cells that run ProcessPoolExecutor.
# Must live in an importable module — spawn-based multiprocessing pickles
# callables by module-path + name, so anything defined in __main__ fails.

import random


def simulate_scenario(seed):
    """Toy Monte Carlo scenario — toy stand-in for one risk simulation."""
    rng = random.Random(seed)
    return sum(rng.gauss(0, 1) for _ in range(10_000))


def benchmark_workload(seed):
    """Lightweight workload used by the strategy-comparison benchmark."""
    rng = random.Random(seed)
    return sum(rng.gauss(0, 1) for _ in range(2_000))
