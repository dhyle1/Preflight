from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer
from preflight.analyzers.models import FileAnalysis
from preflight.metrics.complexity import calculate_complexity


def analyze_file(path: Path) -> FileAnalysis:
    analyzer = ASTAnalyzer(path)
    analyzer.analyze()

    if analyzer.error:
        return FileAnalysis(
            path=path,
            complexity_metrics=[],
            error=analyzer.error,
        )

    if analyzer.tree is None:
        raise RuntimeError("ASTAnalyzer produced no AST")

    complexity_metrics = calculate_complexity(analyzer.tree)

    return FileAnalysis(
        path=path,
        complexity_metrics=complexity_metrics,
        error=None,
    )
