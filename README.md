# Preflight

Preflight is a small Python CLI that runs Ruff, MyPy and Pytest with one command and reports a combined pass/fail result.

The plan is to grow it into a lightweight tool for analyzing code maintainability, but that analysis does not exist yet.

## What it does

Running `preflight` runs these commands, in order, in the current directory:

1. `ruff check .`
2. `mypy src`
3. `pytest`

All three always run, even if an earlier one fails. Their output is printed as-is, followed by a short summary of which checks passed. A check passes if its tool exits with code 0.

## Requirements

- Python 3.11+
- Ruff, MyPy and Pytest installed in the same environment. Preflight calls them by name, so they need to be on your `PATH`.
- Code in a `src/` directory, since MyPy is run on `src`.

If one of the tools isn't installed, Preflight stops with an error instead of reporting a failed check.

## Installation

Clone the repository and install it in editable mode, together with Ruff, MyPy and Pytest:

```bash
pip install -e ".[dev]"
```

## Usage

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

## Exit codes

| Exit code | Description               |
| --------- | ------------------------- |
| 0         | All checks passed         |
| 1         | One or more checks failed |

A check counts as failed whenever its tool exits with a non-zero code.

## Development

Install with the dev dependencies (see [Installation](#installation)), then run the tests:

```bash
pytest
```

Preflight can also be run on itself:

```bash
preflight
```

## Roadmap

See [ROADMAP.md](ROADMAP.md) for where Preflight is heading.
