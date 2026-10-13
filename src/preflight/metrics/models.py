from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionComplexity:
    name: str
    start_line: str
    end_line: str
    complexity: str