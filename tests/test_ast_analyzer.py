from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer


def test_analyze_valid_python(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("x = 1")

    analyzer = ASTAnalyzer(file)

    assert analyzer.analyze() == []