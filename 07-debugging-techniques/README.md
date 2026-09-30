# Python Debugging Techniques

Hands-on notebooks and demo scripts covering Python debugging from first principles — reading tracebacks, using the built-in debugger, debugging inside VS Code, and structured logging for long-running applications.

## Modules

| # | Module | Topics |
|---|--------|--------|
| 01 | [Understanding Python Errors](01-understanding-python-errors/) | Tracebacks, exception types, syntax vs runtime vs logic errors |
| 02 | [Debugging at the Command Line with pdb](02-debugging-at-the-command-line-with-pdb/) | `pdb` module, `breakpoint()`, stepping, inspecting variables, `pdb` commands |
| 03 | [Debugging with Visual Studio Code](03-debugging-with-visual-studio-code/) | Python extension, Run & Debug panel, breakpoints, variable inspection, `launch.json` |
| 04 | [Monitor Python Applications with Logging](04-monitor-python-applications-with-logging/) | `logging` module, log levels, handlers, formatters, `loguru` |

## Notebook

All slide content is consolidated in [`python-debugging-techniques.ipynb`](python-debugging-techniques.ipynb).

## Requirements

```bash
pip install loguru
```
