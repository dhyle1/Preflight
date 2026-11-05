from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionInfo:
    name: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class FunctionMetrics:
    function: FunctionInfo
    complexity: int | None  # None when Radon doesn't score the function
    length: int
