from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionComplexity:
    name: str
    start_line: int
    end_line: int
    complexity: int
