from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer


def test_analyze_valid_python(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("x = 1")

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    assert analyzer.tree is not None
    assert analyzer.functions == []
    assert analyzer.classes == []


def test_analyze_collects_functions_and_classes(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
    "class User:\n"
    "    def login(self):\n"
    "        pass\n"
    "\n"
    "def main():\n"
    "    pass\n"
    )

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    function_names = [function.name for function in analyzer.functions]
    class_names = [cls.name for cls in analyzer.classes]

    assert function_names == ["login", "main"]
    assert class_names == ["User"]


def test_analyze_collects_async_functions(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
        "async def fetch_data():\n"
        "    pass\n"
    )

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    function_names = [function.name for function in analyzer.functions]

    assert function_names == ["fetch_data"]


def test_analyze_stores_syntax_error(tmp_path: Path):
    file = tmp_path / "broken.py"
    file.write_text("def broken(")

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    assert isinstance(analyzer.error, SyntaxError)