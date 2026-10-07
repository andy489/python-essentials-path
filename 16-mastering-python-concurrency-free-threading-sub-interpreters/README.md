# Mastering Python Concurrency: Free Threading & Sub-Interpreters

A comprehensive Jupyter notebook covering Python's modern concurrency model — from GIL internals to free-threaded Python (PEP 703) and sub-interpreters, including profiling and production deployment.

## Notebook

[`python_concurrency_free_threading.ipynb`](python_concurrency_free_threading.ipynb)

## Modules

| # | Module | Topic |
|---|--------|-------|
| 01 | [Understanding the GIL](01-understanding-the-gil/) | Why threads don't scale: GIL mechanics, reference counting, CPU vs I/O, GIL bottleneck proof |
| 02 | [Mixing asyncio with CPU-bound Work](02-mixing-asyncio-with-cpu-bound-work/) | Event-loop starvation, `asyncio.to_thread`, hybrid concurrency patterns |
| 03 | [Running Python Without the GIL](03-running-python-without-the-gil/) | PEP 703 free-threading, per-object locking, biased/deferred ref counting, C-extension compatibility |
| 04 | [Isolating Parallel Work with Sub-Interpreters](04-isolating-parallel-work-with-sub-interpreters/) | `InterpreterPoolExecutor`, isolation vs shared state, callable crossing gotchas |
| 05 | [Profiling Free-Threaded and Sub-Interpreter Workloads](05-profiling-free-threaded-and-sub-interpreter-workloads/) | `BusyMeter`, Amdahl's law, `StackSampler`, benchmark traps |
| 06 | [Shipping Free-Threaded Python to Production](06-shipping-free-threaded-python-to-production/) | asyncio → bounded queue → worker pool, back-pressure, migration gates, production architecture |

## Requirements

- Python 3.13+ (free-threading requires `python3.13t`)
- Jupyter Notebook or JupyterLab

```bash
pip install notebook
jupyter notebook python_concurrency_free_threading.ipynb
```
