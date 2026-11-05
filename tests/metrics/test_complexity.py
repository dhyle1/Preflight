import ast
from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer
from preflight.metrics.complexity import calculate_complexity


def test_calculate_complexity_simple_function():
    source = "def greet():\n    return 'Hello'"

    assert calculate_complexity(ast.parse(source)) == {1: 1}


def test_calculate_complexity_nested_function():
    source = (
        "def outer():\n"
        "    def inner(x):\n"
        "        if x > 10:\n"
        "            return True\n"
        "        return False\n"
        "    return inner(20)\n"
    )

    assert calculate_complexity(ast.parse(source)) == {1: 1, 2: 2}


def test_calculate_complexity_class_method():
    source = (
        "class UserService:\n"
        "    def validate(self, user):\n"
        "        if user.active:\n"
        "            return True\n"
        "        return False\n"
    )

    assert calculate_complexity(ast.parse(source)) == {2: 2}


def test_calculate_complexity_async_function():
    source = (
        "async def fetch_user(user_id):\n"
        "    if user_id <= 0:\n"
        "        return None\n"
        "    return {'id': user_id}\n"
    )

    assert calculate_complexity(ast.parse(source)) == {1: 2}


def test_calculate_complexity_decorated_function_uses_def_line():
    source = (
        "@decorator\n"
        "def greet():\n"
        "    return 'Hello'\n"
    )

    assert calculate_complexity(ast.parse(source)) == {2: 1}


def test_calculate_complexity_does_not_score_local_class_methods():
    source = (
        "def outer():\n"
        "    class Local:\n"
        "        def method(self):\n"
        "            pass\n"
    )

    assert calculate_complexity(ast.parse(source)) == {1: 1}


def test_calculate_complexity_no_functions():
    assert calculate_complexity(ast.parse("x = 10")) == {}


def test_calculate_complexity_with_ast_analyzer(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
        "def check_user(user):\n"
        "    if user.active:\n"
        "        return True\n"
        "    return False\n"
    )

    analyzer = ASTAnalyzer(file)
    analyzer.analyze()

    assert analyzer.error is None
    assert analyzer.tree is not None
    assert calculate_complexity(analyzer.tree) == {1: 2}
