from unittest.mock import patch

from preflight.checks.runner import run_ruff, run_checks, run_pytest, run_mypy


@patch("subprocess.run")
def test_run_ruff_calls_ruff(mock_run):
    run_ruff()

    mock_run.assert_called_once_with(["ruff", "check", "."])


@patch("subprocess.run")
def test_run_pytest_calls_pytest(mock_run):
    run_pytest()

    mock_run.assert_called_once_with(["pytest"])


@patch("subprocess.run")
def test_run_mypy_calls_mypy(mock_run):
    run_mypy()

    mock_run.assert_called_once_with(["mypy", "src"])


@patch("preflight.checks.runner.print_summary")
@patch("preflight.checks.runner.run_mypy")
@patch("preflight.checks.runner.run_pytest")
@patch("preflight.checks.runner.run_ruff")
def test_run_checks_runs_all_checks(
    mock_run_ruff,
    mock_run_pytest,
    mock_run_mypy,
    mock_print_summary
):
    run_checks()

    mock_run_ruff.assert_called_once_with()
    mock_run_pytest.assert_called_once_with()
    mock_run_mypy.assert_called_once_with()
    mock_print_summary.assert_called_once()
