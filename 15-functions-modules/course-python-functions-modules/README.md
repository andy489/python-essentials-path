# reponow package

Features:
- A library that allows you to parse repo locations and map them to a consistent location on disk.
- Several commands to help clone and/or open a repo, via its repo location only:
```sh
wcl https://github.com/g0t4/dotfiles
opener https://github.com/g0t4/dotfiles
```

This package is from a learning exercise for my course at Pluralsight:
TODO link coming soon: [Python: Functions and Modules](https://github.com/g0t4/course-python-functions-modules)


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

FYI I have automated unit tests in the real wcl.py I use, in my dotfiles repo:
https://github.com/g0t4/dotfiles/blob/master/zsh/compat_fish/pythons/wcl.tests.py

```sh

# AND, I have a few examples in test_cases.sh:
./test_cases.sh > expected_test_cases_output
git diff # see if any changes to versioned output file (checked in copy is correct per my wesdemos user)

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
