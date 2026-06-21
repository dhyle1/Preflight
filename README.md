# Preflight

Preflight is a lightweight CLI tool for running project quality checks from a single command.

It currently runs:

* Ruff
* MyPy
* Pytest

and provides a summary of the results and overall check status.

## Installation

Clone the repository and install it in editable mode:

```bash
pip install -e .
```

## Usage

Run Preflight from the root of your project:

```bash
preflight
```

Example output:

```text
✓ Ruff passed
✓ MyPy passed
✓ Pytest passed

Summary
-------
3/3 checks passed
```

## Exit Codes

Preflight returns:

| Exit Code | Description               |
| --------- | ------------------------- |
| 0         | All checks passed         |
| 1         | One or more checks failed |

## Running Tests

```bash
pytest
```

## Roadmap

Planned improvements include:

* Configuration support
* Custom check selection
* Additional quality checks
* CI workflow integration