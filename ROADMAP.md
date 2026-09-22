# Preflight Roadmap

`Next` is realistic near-term work. `Later` is possible future work. Neither is a commitment.

## Where Preflight is today

Preflight runs Ruff, MyPy and Pytest, prints a pass/fail summary, and exits non-zero if any of them fail. Each check only reports whether its tool passed. Preflight doesn't analyze the code itself yet.

## Direction

The goal is for Preflight to analyze the codebase itself, not only run other tools: find maintainability problems such as oversized files and functions or overly complex code, and report them in a way that makes it clear what to fix first.

Preflight will keep using Ruff, MyPy and Pytest for what they already do well rather than reimplementing them.

## Next

- **Structured findings**: let checks report individual findings (file, line, message) instead of only pass/fail. The other items build on this.
- **First analysis checks**: oversized files and functions, and high complexity.
- **Configurable target paths**: instead of the hardcoded `.` and `src`.
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
