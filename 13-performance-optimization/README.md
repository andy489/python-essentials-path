# Python Performance Optimization

A five-part module on making Python code faster, following the **Globomantics** storyline: a team happy with Python whose app is too slow. Course by **Dan Tofan, PhD** ([programmingwithdan.com](https://programmingwithdan.com)).

Everything is consolidated into a single runnable notebook: **[`python-performance-optimization.ipynb`](python-performance-optimization.ipynb)**.

## Sections

| # | Section | Focus |
|---|---------|-------|
| 01 | [Measuring Performance](01-measuring-performance/) | Bottlenecks, `time`/`timeit`, `cProfile`, snakeviz, third-party profilers |
| 02 | [Data Structures and Algorithms](02-data-structures-and-algorithms/) | Big O, lists/arrays, sets/tuples, deques, dicts, named tuples, dataclasses |
| 03 | [Using More Threads](03-using-more-threads/) | `threading`, the GIL, synchronization, when to use threads |
| 04 | [Using Asynchronous Code](04-using-asynchronous-code/) | `asyncio`, coroutines, event loop, `aiohttp`, when to use async |
| 05 | [Using More Processes](05-using-more-processes/) | `multiprocessing`, process communication, choosing a concurrency model |

## The decision in one sentence

**Measure to find the bottleneck; fix it first with a better data structure or algorithm; then, if the work is I/O-bound reach for threads or asyncio, and if it is CPU-bound reach for more processes.**

## Choosing a concurrency model

| | Multiprocessing | Threading / asyncio |
|---|-----------------|---------------------|
| Unit | Multiple processes | Threads / tasks in one process |
| CPU cores | Uses many cores | Effectively one core (GIL) |
| Best for | **CPU-intensive** tasks | **I/O-intensive** tasks |
| Isolation | More isolated | Less isolated |

## Key Concepts

| Concept | Summary |
|---------|---------|
| **Measure first** | *"If you can't measure it, you can't improve it."* Guessing wastes effort |
| **Bottlenecks** | CPU, memory, disk, or network — find which one is the limit |
| **Big O** | How cost grows with input size; O(1) < O(log n) < O(n) < O(n log n) < O(n²) |
| **`cProfile`** | Built-in, general-purpose, deterministic profiler |
| **snakeviz** | Browser-based visualization of `cProfile` output |
| **set / dict** | O(1) membership and key lookup — huge win over scanning a list |
| **deque** | O(1) append/pop at both ends, unlike a list's O(n) front operations |
| **NumPy** | Vectorized numeric arrays, far faster than Python lists for math |
| **GIL** | Only one thread runs Python bytecode at a time; hurts CPU-bound threading |
| **threading** | Helps I/O-bound work (blocking calls release the GIL) |
| **asyncio** | Many I/O tasks in one thread, lower overhead than threads, must stay non-blocking |
| **multiprocessing** | True parallelism across cores for CPU-bound work; no GIL contention |

## Demo Projects

Each section ships with the original course demos, placed directly in the section folder:

- `01-measuring-performance/` — timing loops, a `@profile`-decorated function, memory demo, a `pytest-benchmark` test
- `02-data-structures-and-algorithms/` — before/after Big O comparisons plus list vs. array, deque, dict, set/tuple benchmarks
- `03-using-more-threads/` — threaded downloads, order processing, GIL challenge
- `04-using-asynchronous-code/` — `asyncio` orders, `aiohttp` downloads, async challenge
- `05-using-more-processes/` — `multiprocessing` cleaning tasks, threads vs. processes

Several demos use decorators or command-line profilers (`kernprof`, `snakeviz`) and are meant to be run from a terminal:

```bash
cd 01-measuring-performance
python -m cProfile -o out.prof sum_loop.py
snakeviz out.prof
```

## Running the notebook

```bash
pip install notebook numpy aiohttp
jupyter notebook python-performance-optimization.ipynb
```

The notebook runs top to bottom. NumPy and `aiohttp` cells degrade gracefully if those
packages are missing, and the network-download cell needs internet access.

## Requirements

- Python 3.10+ (uses modern type-hint syntax and f-strings)
- Jupyter Notebook or JupyterLab
- Optional: [`numpy`](https://numpy.org/), [`aiohttp`](https://docs.aiohttp.org/), [`snakeviz`](https://jiffyclub.github.io/snakeviz/), [`line_profiler`](https://github.com/pyutils/line_profiler), [`scalene`](https://github.com/plasma-umass/scalene)
