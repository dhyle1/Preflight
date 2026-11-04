# Preflight Roadmap

`Done` is what exists today. `Next` is realistic near-term work. `Later` is possible future work. Neither `Next` nor `Later` is a commitment.

## Where Preflight is today

Preflight runs Ruff, MyPy and Pytest, prints a pass/fail summary, and exits non-zero if any of them fail. Each check only reports whether its tool passed.

It has also started analyzing the code itself: `preflight analyze [DIR]` reports the cyclomatic complexity of every function in a directory. It only reports the numbers. There are no thresholds, findings or exit codes based on them yet.

## Direction

The goal is for Preflight to analyze the codebase itself, not only run other tools: find maintainability problems such as oversized files and functions or overly complex code, and report them in a way that makes it clear what to fix first.

Preflight will keep using Ruff, MyPy and Pytest for what they already do well rather than reimplementing them.

## Done

- **Combined checks**: `preflight` runs Ruff, MyPy and Pytest, prints a summary, and exits 1 if any fail.
- **File discovery**: `preflight analyze [DIR]` finds `.py` files recursively, skips known tooling directories (`.git`, virtual environments, caches, editor folders, `node_modules`) and doesn't follow symlinked directories.
- **AST parsing**: files are parsed with Python's `ast` module, respecting declared source encodings. Files that can't be read or parsed are reported with an error without stopping the run.
- **Cyclomatic complexity**: computed with Radon for regular, nested and async functions and class methods, and printed per file from most to least complex.

## Next

- **Complexity thresholds**: flag functions above a configurable complexity limit.
- **Structured findings**: let checks and analysis report individual findings (file, line, message) instead of only pass/fail or raw numbers. The other items build on this.
- **CI gating**: make `preflight analyze` exit non-zero when findings exceed the thresholds, so it can fail a build.
- **Size checks**: oversized files and functions.
- **Configurable target paths**: instead of the hardcoded `.` and `src` for the checks.
- **Grouped reporting**: group findings by category and show the worst files first.

## Later

- **More analysis checks**: for example missing type annotations, dead code, duplicate code, and test/coverage signals.
- **Severity levels and ranking**
- **A simple maintainability score**: based on measurable signals, transparent and easy to understand.
- **Branch comparison**: show newly introduced issues and how maintainability metrics change compared to a base branch.

## Out of scope for now

- Web dashboard
- AI-dependent analysis
- IDE integration
- Multi-language support
