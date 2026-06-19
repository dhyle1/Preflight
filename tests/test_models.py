from preflight.checks.models import CheckResult


def test_check_result_passed_for_zero_exit_code():
    result = CheckResult(
        name="Ruff",
        exit_code=0
    )

    assert result.passed is True


def test_check_result_not_passed_for_non_zero_exit_code():
    result = CheckResult(
        name="Ruff",
        exit_code=1
    )

    assert result.passed is False
