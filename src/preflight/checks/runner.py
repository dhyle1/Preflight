import subprocess


def run_ruff() -> int:
    result = subprocess.run(["ruff", "check", "."])
    return result.returncode


def run_pytest() -> int:
    result = subprocess.run(["pytest"])
    return result.returncode


def run_checks() -> None:
    results = {
        "Ruff": run_ruff(),
        "Pytest": run_pytest()
    }

    print_summary(results)


def print_summary(check_results: dict[str, int]) -> None:
    passed = 0

    for name, code in check_results.items():
        status = 'passed' if code == 0 else 'failed'
        symbol = '✓' if code == 0 else 'x'

        print(f"{symbol} {name} {status}")

        if code == 0:
            passed += 1

    print("\nSummary")
    print("-------")
    print(f"{passed}/{len(check_results)} checks passed")

