from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer
from preflight.metrics.models import FunctionInfo


def _analyze_source(tmp_path: Path, source: str) -> ASTAnalyzer:
    file = tmp_path / "example.py"
    file.write_text(source)

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    return analyzer


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

    assert function_names == ["User.login", "main"]
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


def test_analyze_qualifies_nested_names(tmp_path: Path):
    analyzer = _analyze_source(
        tmp_path,
        "class Outer:\n"
        "    class Nested:\n"
        "        def nested_method(self):\n"
        "            pass\n"
        "\n"
        "    def method(self):\n"
        "        def closure():\n"
        "            pass\n"
        "\n"
        "def function():\n"
        "    def inner():\n"
        "        pass\n",
    )

    assert [function.name for function in analyzer.functions] == [
        "Outer.Nested.nested_method",
        "Outer.method",
        "Outer.method.closure",
        "function",
        "function.inner",
    ]


def test_analyze_scope_does_not_leak_to_later_functions(tmp_path: Path):
    analyzer = _analyze_source(
        tmp_path,
        "class First:\n"
        "    def method(self):\n"
        "        pass\n"
        "\n"
        "def after():\n"
        "    pass\n",
    )

    assert analyzer.functions[-1].name == "after"


def test_analyze_end_line_includes_nested_definitions(tmp_path: Path):
    analyzer = _analyze_source(
        tmp_path,
        "def outer():\n"
        "    x = 1\n"
        "    def inner():\n"
        "        pass\n",
    )

    assert analyzer.functions[0] == FunctionInfo("outer", 1, 4)


def test_analyze_end_line_includes_multiline_string(tmp_path: Path):
    analyzer = _analyze_source(
        tmp_path,
        "def text():\n"
        '    return """\n'
        "    body\n"
        '    """\n',
    )

    assert analyzer.functions[0] == FunctionInfo("text", 1, 4)


def test_analyze_decorated_function_starts_at_def(tmp_path: Path):
    analyzer = _analyze_source(
        tmp_path,
        "@decorator\n"
        "@other(\n"
        "    1,\n"
        ")\n"
        "def decorated():\n"
        "    pass\n",
    )

    assert analyzer.functions[0] == FunctionInfo("decorated", 5, 6)


def test_analyze_stores_syntax_error(tmp_path: Path):
    file = tmp_path / "broken.py"
    file.write_text("def broken(")

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    assert isinstance(analyzer.error, SyntaxError)