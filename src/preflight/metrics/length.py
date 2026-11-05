from preflight.metrics.models import FunctionInfo


def calculate_length(function: FunctionInfo) -> int:
    return function.end_line - function.start_line + 1
