import subprocess

from preflight.checks.models import CheckResult


def run_checks() -> None:
    results = [
        run_ruff(),
        run_mypy(),
        run_pytest()
    ]

    print_summary(results)


def run_ruff() -> CheckResult:
    result = subprocess.run(["ruff", "check", "."])

    return CheckResult(
        name="Ruff",
        exit_code=result.returncode
    )


def run_mypy() -> CheckResult:
    result = subprocess.run(["mypy", "src"])

    return CheckResult(
        name="MyPy",
        exit_code=result.returncode
    )


def run_pytest() -> CheckResult:
    result = subprocess.run(["pytest"])

    return CheckResult(
        name="Pytest",
        exit_code=result.returncode
    )


def print_summary(check_results: list[CheckResult]) -> None:
    passed = 0
    
    for result in check_results:
        status = "passed" if result.passed else "failed"
        symbol = "✓" if result.passed else "x"

        print(f"{symbol} {result.name} {status}")

        if result.passed:
            passed += 1

    print("\nSummary")
    print("-------")
    print(f"{passed}/{len(check_results)} checks passed")

