import subprocess

from preflight.checks.models import CheckResult


def run_checks() -> int:
    results = [
        run_ruff(),
        run_mypy(),
        run_pytest()
    ]

    print_summary(results)

    return 0 if all_checks_passed(results) else 1


def run_ruff() -> CheckResult:
    return run_tool("Ruff", ["ruff", "check", "."])


def run_mypy() -> CheckResult:
    return run_tool("MyPy", ["mypy", "src"])


def run_pytest() -> CheckResult:
    return run_tool("Pytest", ["pytest"])


def run_tool(name: str, command: list[str]) -> CheckResult:
    try:
        result = subprocess.run(command, check=False)
    except FileNotFoundError:
        return CheckResult(name=name, exit_code=127, tool_missing=True)

    return CheckResult(name=name, exit_code=result.returncode)


def all_checks_passed(check_results: list[CheckResult]) -> bool:
    return all(result.passed for result in check_results)


def print_summary(check_results: list[CheckResult]) -> None:
    passed = 0
    
    for result in check_results:
        status = "passed" if result.passed else "failed"
        symbol = "✓" if result.passed else "x"

        if result.tool_missing:
            status = "not found (is it installed and on PATH?)"

        print(f"{symbol} {result.name} {status}")

        if result.passed:
            passed += 1

    print("\nSummary")
    print("-------")
    print(f"{passed}/{len(check_results)} checks passed")

