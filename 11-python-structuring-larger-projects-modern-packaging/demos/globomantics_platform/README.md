# Globomantics Platform (Organized Demo)

This is the organized, scalable version of the Globomantics customer
billing and analytics system.

Key characteristics:

- `src/` layout
- Clear domain packages: data, analytics, billing, notifications, plugins
- A separate CLI package (`globomantics_cli`) wired via `pyproject.toml` entry point
- Test suite under `tests/`

Run locally with:

```bash
pip install -e ".[dev]"
globomantics-cli
