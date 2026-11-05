# Preflight

Preflight is a small Python CLI with two commands:

- `preflight` runs Ruff, MyPy and Pytest with one command and reports a combined pass/fail result.
- `preflight analyze [DIR]` finds the Python files in a directory and reports the cyclomatic complexity and length of each function.

The plan is to grow it into a lightweight tool for analyzing code maintainability. For now, `analyze` only reports numbers: there are no thresholds, findings or pass/fail results for it yet.

## What it does

### Running checks

Running `preflight` runs these commands, in order, in the current directory:

1. `ruff check .`
2. `mypy src`
3. `pytest`

All three always run, even if an earlier one fails. Their output is printed as-is, followed by a short summary of which checks passed. A check passes if its tool exits with code 0.

### Analyzing functions

Running `preflight analyze [DIR]` walks `DIR` (the current directory by default), parses every `.py` file it finds, and prints two metrics for each function: its cyclomatic complexity, computed with [Radon](https://radon.readthedocs.io/), and its length.

- Regular, nested and async functions are included, as well as class methods. Methods are shown as `ClassName.method` and nested functions as `outer.inner`.
- Length is the physical line span from the `def` line to the function's last statement. It includes blank lines and docstrings, and excludes decorators and comments after the last statement. A nested function counts toward both itself and its parent.
- Radon doesn't score methods of classes defined inside a function, and doesn't add them to the parent's complexity. They are listed with their length and `-` for complexity.
- Files are read using their declared source encoding (for example `# -*- coding: latin-1 -*-`), defaulting to UTF-8.
- Files that can't be read or parsed are listed with an error, and the rest are still analyzed.
- Symlinked directories aren't followed, and these directories are skipped at any depth: `.git`, `.venv`, `venv`, `.env`, `__pycache__`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `.tox`, `.nox`, `.idea`, `.vscode` and `node_modules`.

## Requirements

- Python 3.11+
- Radon, which is installed automatically as a dependency.
- For `preflight` only:
  - Ruff, MyPy and Pytest installed in the same environment. Preflight calls them by name, so they need to be on your `PATH`.
  - Code in a `src/` directory, since MyPy is run on `src`.

If one of the tools isn't installed, Preflight reports that check as failed with a "not found" message and still runs the others.

## Installation

Clone the repository and install it in editable mode, together with Ruff, MyPy and Pytest:

```bash
pip install -e ".[dev]"
```

## Usage

### `preflight`

Run Preflight from the root of the project you want to check:

```bash
preflight
```

The output from each tool comes first, followed by Preflight's summary:

```text
... output from ruff, mypy and pytest ...
✓ Ruff passed
x MyPy failed
✓ Pytest passed

Summary
-------
2/3 checks passed
```

### `preflight analyze`

```bash
preflight analyze          # analyze the current directory
preflight analyze src/     # analyze a specific directory
```

Files are listed in path order. Within each file, functions are sorted from most to least complex, with their starting line (`LINE`), cyclomatic complexity (`CC`) and length in lines (`LEN`). Functions without a complexity score come last. A summary at the end gives the totals and the most complex function, if any were scored:

```text
Preflight Analysis
-----------------------------------------------------------------

pkg/__init__.py
  No functions found.

pkg/orders.py
                  LINE    CC   LEN
  Order.validate     2     4     6
  load.parse        10     2     3
  load               9     1     5

pkg/utils.py
  Error: invalid syntax (<unknown>, line 1)

Summary
-------
Files:        3
Functions:    3
Errors:       1
Most complex: Order.validate (CC 4) at pkg/orders.py:2
```

## Exit codes

For `preflight`:

| Exit code | Description               |
| --------- | ------------------------- |
| 0         | All checks passed         |
| 1         | One or more checks failed |

A check counts as failed whenever its tool exits with a non-zero code or isn't installed.

For `preflight analyze`:

| Exit code | Description                                       |
| --------- | ------------------------------------------------- |
| 0         | Analysis finished, whatever the complexity values |
| 1         | The given path isn't a directory                  |

## Limitations

- `analyze` only reports numbers. It has no complexity thresholds, doesn't produce findings, and can't fail a build, so it isn't usable as a CI gate yet.
- `analyze` only takes a directory, not a single file.
- Complexity and function length are the only metrics so far. File size isn't measured yet.
- The `preflight` checks always run on `.` and `src`. Their paths can't be configured.
- There is no configuration file.

## Development

Install with the dev dependencies (see [Installation](#installation)), then run the tests:

```bash
pytest
```

Preflight can also be run on itself:

```bash
preflight
preflight analyze src/
```

## Roadmap

See [ROADMAP.md](ROADMAP.md) for what's done and where Preflight is heading.
