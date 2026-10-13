from dataclasses import dataclass
from pathlib import Path

from preflight.metrics.models import FunctionComplexity


@dataclass(frozen=True)
class FileAnalysis:
    path: Path
    complexity_metrics: list[FunctionComplexity]
    error: Exception | None
