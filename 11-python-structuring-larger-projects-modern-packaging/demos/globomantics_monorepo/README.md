# Globomantics Monorepo (Demo)

This repository simulates a real Python monorepo containing multiple
independently installable packages:

- globomantics_shared
- globomantics_data
- globomantics_analytics
- globomantics_billing
- globomantics_plugins
- globomantics_cli

Each package has its own `pyproject.toml` and versioning strategy, but all
share a common domain model