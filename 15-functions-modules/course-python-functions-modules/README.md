# reponow package

Features:
- A library that allows you to parse repo locations and map them to a consistent location on disk.
- Several commands to help clone and/or open a repo, via its repo location only:
```sh
wcl https://github.com/andy489/python-essentials-path
opener https://github.com/andy489/python-essentials-path
```

This package is a learning exercise covering Python functions and modules.


## Install

```sh
pipx install reponow
wcl ...
opener ...
```

## Build

### Setup .venv w/ dependencies

```sh
# use uv for dependencies
uv sync

# OR, use venv/pip manually
python3 -m venv .venv
source .venv/bin/activate
# source .venv/bin/activate.fish  # if using fish shell
pip3 install .
```

### Run commands

```sh
# always make sure your venv is activated
source .venv/bin/activate[.fish]

# run commands "standalone"
uv pip install --editable .
# --editable allows you to change the code, w/o re-installing it
wcl ...
opener ...

# cloner, pick one:
python3 reponow/wcl.py
python3 -m reponow.wcl
python3 -m reponow # thanks to __main__.py

# opener, pick one:
python3 reponow/opener.py
python3 -m reponow.opener
```

### Test wcl

```sh
# A few examples in test_cases.sh:
./test_cases.sh > expected_test_cases_output
git diff # see if any changes to versioned output file

# double check expected matches what's in test_cases.sh
icdiff test_cases.sh expected_test_cases_output
# then look for commmented out paths to line up (obviously not the full script)
```

### pytest for pathz

```sh
# run one time:
pytest

# watch for changes, and re-run tests:
ptw
ptw pathz # subset
```
