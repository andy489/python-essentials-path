# Python: Structuring Larger Projects with Modern Packaging

A six-part module covering how to grow Python projects from a single script into a well-structured, packaged, and maintainable system.

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | From Scripts to Scalable Systems | `src` layout, monorepo vs. multi-package strategies |
| 02 | Dependency Management and Security Scanning | `pyproject.toml`, Poetry, pip-tools, lock files, pip-audit |
| 03 | Packaging and Advanced Distribution | PEP 621, build backends (setuptools/hatch/flit), sdist, wheel, twine |
| 04 | CI/CD for Scalable Project Workflows | GitHub Actions, matrix builds, trusted publishing (OIDC), MkDocs |
| 05 | Quality Gates and Type Safety at Scale | mypy, pyright, ruff, automated quality gate pipeline |
| 06 | Extensibility and Plug-in Architectures | Entry points, dependency inversion, dynamic plugin loading |

## Key Concepts

| Concept | Summary |
|---------|---------|
| **`src` layout** | Prevents import accidents; enforces installation before use |
| **`pyproject.toml` (PEP 621)** | Single source of truth for metadata, dependencies, and tool config |
| **Lock files** | Guarantee reproducible installs across machines and CI |
| **Build backends** | setuptools (flexible), hatch (modern), flit (minimal) |
| **Trusted Publishing** | OIDC-based PyPI auth — no long-lived tokens needed |
| **Quality gates** | lint → format → typecheck → test → security scan; all must pass |
| **Entry points** | Plugins self-register via `pyproject.toml`; discovered at runtime |

## Demo Projects

The `demos/` folder contains three self-contained Python projects used throughout the course:

- `demos/globomantics_legacy/` — flat-layout legacy script (the "before" state)
- `demos/globomantics_platform/` — single `src`-layout package with tests and multiple build backend configs
- `demos/globomantics_monorepo/` — full monorepo with `billing`, `analytics`, `plugins`, `shared`, CI, and MkDocs

### Running the demos

```bash
cd demos/globomantics_platform
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Companion Notebook

`from-scripts-to-scalable-systems.ipynb` — covers all six modules with explanations and runnable code examples.

```bash
pip install notebook
jupyter notebook from-scripts-to-scalable-systems.ipynb
```

## Requirements

- Python 3.11+
- Jupyter Notebook or JupyterLab

```bash
pip install notebook
jupyter notebook
```
