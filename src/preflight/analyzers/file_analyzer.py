from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer
from preflight.analyzers.models import FileAnalysis
from preflight.metrics.complexity import calculate_complexity
from preflight.metrics.length import calculate_length
from preflight.metrics.models import FunctionMetrics


def analyze_file(path: Path) -> FileAnalysis:
    analyzer = ASTAnalyzer(path)
    analyzer.analyze()

    if analyzer.error:
        return FileAnalysis(
            path=path,
            function_metrics=[],
            error=analyzer.error,
        )

    if analyzer.tree is None:
        raise RuntimeError("ASTAnalyzer produced no AST")

    complexities = calculate_complexity(analyzer.tree)

    function_metrics = [
        FunctionMetrics(
            function=function,
            complexity=complexities.get(function.start_line),
            length=calculate_length(function),
        )
        for function in analyzer.functions
    ]

    return FileAnalysis(
        path=path,
        function_metrics=function_metrics,
        error=None,
    )
