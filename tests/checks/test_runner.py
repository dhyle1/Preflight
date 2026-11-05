from unittest.mock import Mock, patch

import pytest

from preflight.checks.models import CheckResult
from preflight.checks.runner import (
    all_checks_passed,
    print_summary,
    run_checks,
    run_mypy,
    run_pytest,
    run_ruff,
)


@patch("subprocess.run")
def test_run_ruff_calls_ruff(mock_run):
    run_ruff()

    mock_run.assert_called_once_with(["ruff", "check", "."], check=False)


@patch("subprocess.run")
def test_run_mypy_calls_mypy(mock_run):
    run_mypy()

    mock_run.assert_called_once_with(["mypy", "src"], check=False)


@patch("subprocess.run")
def test_run_pytest_calls_pytest(mock_run):
    run_pytest()

    mock_run.assert_called_once_with(["pytest"], check=False)


@pytest.mark.parametrize(
    ("run_check", "name"),
    [(run_ruff, "Ruff"), (run_mypy, "MyPy"), (run_pytest, "Pytest")],
)
@patch("subprocess.run", side_effect=FileNotFoundError)
def test_run_check_reports_missing_tool(mock_run, run_check, name):
    result = run_check()

    assert result.name == name
    assert result.tool_missing is True
    assert result.passed is False


@patch("subprocess.run", return_value=Mock(returncode=127))
def test_run_check_exit_code_127_is_not_a_missing_tool(mock_run):
    result = run_pytest()

    assert result.exit_code == 127
    assert result.tool_missing is False
    assert result.passed is False


@patch("subprocess.run")
def test_run_checks_continues_after_missing_tool(mock_run, capsys):
    mock_run.side_effect = [
        FileNotFoundError,
        Mock(returncode=0),
        Mock(returncode=0),
    ]

    assert run_checks() == 1
    assert mock_run.call_count == 3

    output_lines = capsys.readouterr().out.splitlines()

    assert "x Ruff not found (is it installed and on PATH?)" in output_lines
    assert "✓ MyPy passed" in output_lines
    assert "✓ Pytest passed" in output_lines
    assert "2/3 checks passed" in output_lines


def test_print_summary_ordinary_failure_says_failed(capsys):
    print_summary([CheckResult("Pytest", 127)])

    output_lines = capsys.readouterr().out.splitlines()

    assert "x Pytest failed" in output_lines


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

