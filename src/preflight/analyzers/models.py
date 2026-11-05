from dataclasses import dataclass
from pathlib import Path

from preflight.metrics.models import FunctionMetrics


@dataclass(frozen=True)
class FileAnalysis:
    path: Path
    function_metrics: list[FunctionMetrics]
    error: Exception | None
