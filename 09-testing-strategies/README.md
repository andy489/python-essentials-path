# Python Testing Strategies

A three-part module on building a robust Python testing strategy, using a Phonebook application as the running demo.

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Using Pytest to Create Unit Tests](01-using-pytest-to-create-unit-tests/) | pytest basics, assertions, fixtures, parameterized tests |
| 02 | [Using Test Doubles](02-using-test-doubles/) | Stubs, fakes, spies, dummies with `unittest.mock` |
| 03 | [Integration Tests and Functional Tests](03-integration-tests-and-functional-tests/) | Hexagonal architecture, narrow integration tests, functional tests |

## The Testing Pyramid

```
        /\
       /  \       ← Functional tests  (fewest, exercise most)
      /----\
     /      \     ← Narrow integration tests
    /--------\
   /          \   ← Unit tests        (most, exercise least)
  /____________\
```

## Key Concepts

| Concept | Summary |
|---------|---------|
| **pytest** | Readable, scalable test framework; use plain `assert` |
| **Fixtures** | `@pytest.fixture` for shared setup, injected by parameter name |
| **Parametrize** | `@pytest.mark.parametrize` to run one test with many inputs |
| **Stub** | Returns a canned response — no real logic |
| **Fake** | Working simplified implementation (e.g. `StringIO` instead of a file) |
| **Spy** | Records calls so you can assert on side effects |
| **Dummy** | Passed to satisfy a signature but never actually called |
| **Hexagonal architecture** | Separates domain code from adapters via inbound/outbound ports |
| **Narrow integration tests** | Test one adapter against its real external service |
| **Functional tests** | Full user workflow end to end; use sparingly |

## Demo Projects

Each section includes a self-contained Python project with `pyproject.toml` and a `tests/` directory:

- `01-using-pytest-to-create-unit-tests/phonebook_demo/`
- `02-using-test-doubles/phonebook_demo_m2/`
- `03-integration-tests-and-functional-tests/phonebook_demo_m3/`

### Running the demos

```bash
cd 01-using-pytest-to-create-unit-tests/phonebook_demo
uv run pytest
```

## Requirements

- Python 3.8+
- [`uv`](https://github.com/astral-sh/uv) (or `pip install pytest`)
- Jupyter Notebook or JupyterLab for the companion notebook

```bash
pip install notebook
jupyter notebook python-testing-strategies.ipynb
```
