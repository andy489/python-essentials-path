# Python Clean Code Practices

A five-part module on writing Python that stays readable, maintainable, and reviewable over time. Course by **Reindert-Jan Ekker** ([www.codesensei.nl](https://www.codesensei.nl)).

Everything is consolidated into a single runnable notebook: **[`python-clean-code-practices.ipynb`](python-clean-code-practices.ipynb)**.

## Sections

| # | Section | Focus |
|---|---------|-------|
| 01 | [Writing Maintainable Python Code](01-writing-maintainable-python-code/) | Quality attributes, KISS, YAGNI, SRP, cohesion, coupling, DRY, naming |
| 02 | [Python Style Guidelines & PEP 8](02-python-style-guidelines-and-pep8/) | Layout, imports, naming, tooling (ruff, black) |
| 03 | [Documenting Your Project](03-documenting-your-python-project/) | Docstrings (PEP 257), Google/NumPy/Sphinx styles |
| 04 | [Error Handling & Exceptions](04-error-handling-and-exceptions/) | try/except, EAFP, custom exceptions, layering, `raise from` |
| 05 | [Effective Code Reviews](05-effective-code-reviews/) | The code review pyramid, constructive feedback |

## The Code Review Pyramid

```
                    Style                     <- automate (ruff/black)
                   Testing                    <- partly automate (CI, coverage)
                Documentation
           Behaviour and Correctness
          Design and Architecture             <- most important, hardest to automate
```

Spend review attention at the bottom (design), and automate the top (style).

## Key Concepts

| Concept | Summary |
|---------|---------|
| **KISS** | Keep it short and simple — the simplest thing that works |
| **YAGNI** | You aren't gonna need it — don't build for imagined futures |
| **SRP** | Single responsibility — one job you can name in a sentence |
| **Cohesion / Coupling** | Aim for high cohesion, loose coupling |
| **DRY** | Don't repeat yourself — one source of truth per fact |
| **PEP 8** | Style guide: 4-space indent, 79-char lines, naming conventions |
| **PEP 257** | Docstring conventions: triple quotes, phrase ending in a period |
| **EAFP** | Easier to ask forgiveness than permission — try, then handle failure |
| **`raise ... from`** | Chain exceptions to preserve the original cause |
| **Layered handling** | Catch exceptions where you have the context to handle them |
| **Review pyramid** | Design > correctness > docs > tests > style |

## Demo Projects

Each section ships with the original course demos:

- `01-writing-maintainable-python-code/demos/principles/` — coupling, dataclasses, YAGNI, naming
- `02-python-style-guidelines-and-pep8/demos/` — before/after `gamedemo` with `ruff.toml`
- `03-documenting-your-python-project/demos/` — a `gamedemo` package with a built Sphinx `docs/`
- `04-error-handling-and-exceptions/demos/error_handling/` — layered user-management example

## Running the notebook

```bash
pip install notebook
jupyter notebook python-clean-code-practices.ipynb
```

The notebook is self-contained — every code cell runs top to bottom with only the standard library. All 27 code cells execute cleanly.

## Requirements

- Python 3.10+ (uses `list[...]` and `X | Y` type-hint syntax)
- Jupyter Notebook or JupyterLab for the companion notebook
- Optional tooling referenced in the modules: [`ruff`](https://docs.astral.sh/ruff/), [`black`](https://black.readthedocs.io/), [`sphinx`](https://www.sphinx-doc.org/)
