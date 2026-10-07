# 15 — Functions and Modules

Hands-on exploration of Python functions and the module/package system, built around the `reponow` and `pathz` real-world packages from the companion course.

## Topics

- **Functions** — definition, first-class objects, default parameters, `*args`/`**kwargs`, keyword-only and positional-only parameters, multiple return values, `lambda`, `global`/`nonlocal`
- **Imports** — `import module`, `from module import name`, aliases, `__all__`, avoiding namespace pollution
- **Module internals** — `__name__`, `__file__`, dunder attributes, `sys.modules`, `sys.path`, the `if __name__ == "__main__"` guard
- **Packages** — `__init__.py` as a public API surface, relative vs absolute imports, `__main__.py` and `python -m`
- **Modern packaging** — `pyproject.toml` (PEP 517/518), build backends, `uv`, editable installs
- **Decorators** — wrapping stdlib functions to extend behavior transparently
- **Testing** — `pytest` with `@pytest.mark.parametrize` for table-driven test cases

## Files

| File | Description |
|------|-------------|
| `python_functions_modules.ipynb` | Main notebook with all demos |
| `course-python-functions-modules/` | Course project: `reponow` and `pathz` packages |
| `demos.txt` | Link to the upstream course repository |

## Course project

The `reponow` package clones or opens a repo given only its URL, mapping it to a consistent local path:

```sh
wcl https://github.com/torvalds/linux
opener https://github.com/g0t4/dotfiles
```

The `pathz` package wraps `os.path` functions so that `~/path` tilde-expansion is automatic.

## Requirements

- Python 3.8+
- Jupyter Notebook or JupyterLab (`pip install notebook`)
- `uv` (optional, for running the course project)
