# Mastering Python Concurrency: Free-threading & Sub-interpreters

A deep dive into modern Python concurrency, covering the GIL's internals, the free-threaded build (PEP 703), sub-interpreters (PEP 684/734), asyncio hybrid patterns, profiling, and production deployment strategies.

## Notebook

**`mastering_python_concurrency.ipynb`** — Single comprehensive notebook synthesising all six modules. Covers theory, runnable demos, and production patterns end-to-end.

`_nb_workers.py` — Helper module required by notebook cells that use `ProcessPoolExecutor`. macOS spawns worker processes fresh, so worker callables must live in an importable file rather than the notebook's `__main__`.

### Requirements

- Python 3.11+ for most cells
- Python 3.14 / 3.14t (`python3.14t`) for free-threading and `InterpreterPoolExecutor` cells
- Jupyter Notebook or JupyterLab

```bash
pip install notebook
jupyter notebook mastering_python_concurrency.ipynb
```

## Modules

| # | Folder | Topic |
|---|--------|-------|
| 1 | [01-understanding-the-gil-why-threads-dont-scale](01-understanding-the-gil-why-threads-dont-scale/) | GIL internals, ref-counting, why CPU-bound threads don't scale, process pools as the escape hatch |
| 2 | [02-mixing-asyncio-with-cpu-bound-work](02-mixing-asyncio-with-cpu-bound-work/) | asyncio execution model, event-loop starvation, `asyncio.to_thread()`, async ingestion layer |
| 3 | [03-running-python-without-the-gil](03-running-python-without-the-gil/) | Free-threaded build (PEP 703/779), per-object locking, biased ref-counting, `sys._is_gil_enabled()` |
| 4 | [04-isolating-parallel-work-with-sub-interpreters](04-isolating-parallel-work-with-sub-interpreters/) | Sub-interpreters (PEP 684/734), one GIL per interpreter, `InterpreterPoolExecutor`, data crossing boundaries |
| 5 | [05-profiling-free-threaded-and-sub-interpreter-workloads](05-profiling-free-threaded-and-sub-interpreter-workloads/) | Benchmark methodology, Amdahl's Law, cores-used metric, comparing all four concurrency strategies |
| 6 | [06-shipping-free-threaded-python-to-production](06-shipping-free-threaded-python-to-production/) | 4-gate rollout, C-extension audit, dual-build CI, feature-flagged GIL, production risk engine, observability |

### Demo files per module

Each module folder contains a `demos/` directory with the original course demo scripts referenced by the notebook.

**Module 1** — Orienting to the Globomantics risk engine · Proving the GIL bottleneck · Offloading CPU work off the event loop · Adding an async ingestion layer

**Module 2** — Adding an async ingestion layer · Offloading CPU work off the event loop · Running on the free-threaded build · New race conditions, new rules · Detecting data races before they ship

**Module 3** — Running on the free-threaded build · New race conditions, new rules · Detecting data races before they ship

**Module 4** — Running simulations in sub-interpreters · Passing data across the isolation boundary

**Module 5** — Profiling the risk engine · Comparing all four strategies

**Module 6** — Assembling the production risk engine · Failure handling and observability
