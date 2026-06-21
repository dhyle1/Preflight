from unittest.mock import patch

from preflight.checks.models import CheckResult
from preflight.checks.runner import (
    run_ruff,
    run_mypy,
    run_pytest,
    run_checks,
    all_checks_passed
)


@patch("subprocess.run")
def test_run_ruff_calls_ruff(mock_run):
    run_ruff()

    mock_run.assert_called_once_with(["ruff", "check", "."])


@patch("subprocess.run")
def test_run_mypy_calls_mypy(mock_run):
    run_mypy()

    mock_run.assert_called_once_with(["mypy", "src"])


@patch("subprocess.run")
def test_run_pytest_calls_pytest(mock_run):
    run_pytest()

    mock_run.assert_called_once_with(["pytest"])


@patch("preflight.checks.runner.print_summary")
@patch("preflight.checks.runner.run_pytest")
@patch("preflight.checks.runner.run_mypy")
@patch("preflight.checks.runner.run_ruff")
def test_run_checks_runs_all_checks(
    mock_run_ruff,
    mock_run_mypy,
    mock_run_pytest,
    mock_print_summary,
):
    mock_run_ruff.return_value = CheckResult("Ruff", 0)
    mock_run_mypy.return_value = CheckResult("MyPy", 0)
    mock_run_pytest.return_value = CheckResult("Pytest", 0)

    run_checks()

    mock_run_ruff.assert_called_once_with()
    mock_run_mypy.assert_called_once_with()
    mock_run_pytest.assert_called_once_with()
    mock_print_summary.assert_called_once()


@patch("preflight.checks.runner.print_summary")
@patch("preflight.checks.runner.run_pytest")
@patch("preflight.checks.runner.run_mypy")
@patch("preflight.checks.runner.run_ruff")
def test_run_checks_returns_zero_when_all_passes(
    mock_run_ruff,
    mock_run_mypy,
    mock_run_pytest,
    mock_print_summary,
):
    mock_run_ruff.return_value = CheckResult("Ruff", 0)
    mock_run_mypy.return_value = CheckResult("MyPy", 0)
    mock_run_pytest.return_value = CheckResult("Pytest", 0)

    assert run_checks() == 0


@patch("preflight.checks.runner.print_summary")
@patch("preflight.checks.runner.run_pytest")
@patch("preflight.checks.runner.run_mypy")
@patch("preflight.checks.runner.run_ruff")
def test_run_checks_returns_one_when_any_fails(
    mock_run_ruff,
    mock_run_mypy,
    mock_run_pytest,
    mock_print_summary,
):
    mock_run_ruff.return_value = CheckResult("Ruff", 1)
    mock_run_mypy.return_value = CheckResult("MyPy", 0)
    mock_run_pytest.return_value = CheckResult("Pytest", 0)

    assert run_checks() == 1


def test_all_checks_passed_returns_true_when_all_passes():
    results = [
        CheckResult("Ruff", 0),
        CheckResult("MyPy", 0)
    ]

    assert all_checks_passed(results) is True


def test_all_checks_passed_returns_false_when_any_fails():
    results = [
        CheckResult("Ruff", 1),
        CheckResult("MyPy", 0)
    ]

    assert all_checks_passed(results) is False

