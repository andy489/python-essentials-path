# 18 — Functional Programming in Python

Hands-on exploration of the six core functional programming principles applied in Python, based on Gerald Britton's Pluralsight course.

## Topics

- **Introduction** — programming paradigms (imperative, procedural, OOP, declarative, logic, functional); FP history (Lisp → APL → ML → Haskell); the six FP principles
- **First-class functions** — functions as values; higher-order functions; composition, closures, and currying; `functools.partial`; `map`, `filter`, `sorted`
- **Pure functions** — side-effect elimination; single responsibility; same input → same output; lambdas vs. named helpers; bytecode analysis with `dis`
- **Immutable variables** — local variables never change; `tuple`, `frozenset`, `@dataclass(frozen=True)`; custom `Immutable` ABC using `__slots__` and `frozenset`
- **Lazy evaluation** — eager vs. lazy trade-offs; Python's lazy evolution (`xrange` → iterators → generators → `yield from`); `itertools.islice`, `itertools.tee`, `itertools.chain`
- **Recursion** — mathematical recurrence relations; basic recursion; tail-call accumulator pattern; trampolining to work around Python's stack limit; `functools.reduce`
- **Pattern matching** — `match`/`case` (Python 3.10+); literal, type, OR, guard, capture, sequence, mapping, and class patterns; `@dataclass` validation with `__post_init__`

## Files

| File / Folder | Description |
|---------------|-------------|
| `functional_programming_python.ipynb` | Main notebook — all concepts with runnable examples |
| `01-introduction-to-functional-programming/` | Paradigms overview, FP history, six principles |
| `02-first-class-functions/` | Composition, closures, currying demos (`currying.py`, `getints.py`) |
| `03-pure-functions/` | Side-effect elimination; Before/After refactoring demos |
| `04-immutable-variables/` | Immutable ABC (`immutable.py`); frozen dataclass pattern |
| `05-lazy-evaluation/` | Generator demos; eager vs. lazy comparison |
| `06-recursion/` | Fibonacci variants (`fibonacci.py`, `fibonacci_tail.py`, `fibonacci_tramp.py`); trampolining (`tramp.py`) |
| `07-pattern-matching/` | Match examples (`match_examples.py`, `match_validation.py`); F#/Haskell/SQL comparisons |

Each module folder contains:

```
<module>/demos/
    Before/     — starting code before applying the FP principle
    After/      — refactored code applying the principle
    Examples/   — standalone examples from the slides
    Assignment/ — practice assignment with solution
```

## Requirements

- Python 3.10+ (pattern matching requires 3.10)
- Jupyter Notebook or JupyterLab (`pip install notebook`)
