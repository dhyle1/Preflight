from preflight.metrics.length import calculate_length
from preflight.metrics.models import FunctionInfo


def test_calculate_length_single_line():
    function = FunctionInfo(name="one_liner", start_line=5, end_line=5)

    assert calculate_length(function) == 1


def test_calculate_length_counts_every_line_in_span():
    function = FunctionInfo(name="process", start_line=10, end_line=19)

    assert calculate_length(function) == 10
