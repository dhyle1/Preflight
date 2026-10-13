import ast
from pathlib import Path

from preflight.analyzers.ast_analyzer import ASTAnalyzer
from preflight.metrics.complexity import calculate_complexity


def test_calculate_complexity_simple_function():
    source = "def greet():\n    return 'Hello'"

    tree = ast.parse(source)
    results = calculate_complexity(tree)

    assert len(results) == 1
    assert results[0].name == "greet"
    assert results[0].start_line == 1
    assert results[0].end_line == 2
    assert results[0].complexity == 1


def test_calculate_complexity_nested_function():
    source = (
        "def outer():\n"
        "    def inner(x):\n"
        "        if x > 10:\n"
        "            return True\n"
        "        return False\n"
        "    return inner(20)\n"
    )

    tree = ast.parse(source)
    results = calculate_complexity(tree)

    assert len(results) == 2

    assert results[0].name == "outer"
    assert results[0].start_line == 1
    assert results[0].end_line == 6
    assert results[0].complexity == 1

    assert results[1].name == "outer.inner"
    assert results[1].start_line == 2
    assert results[1].end_line == 5
    assert results[1].complexity == 2


def test_calculate_complexity_class_method():
    source = (
        "class UserService:\n"
        "    def validate(self, user):\n"
        "        if user.active:\n"
        "            return True\n"
        "        return False\n"
    )

    tree = ast.parse(source)
    results = calculate_complexity(tree)

    assert len(results) == 1
    assert results[0].name == "UserService.validate"
    assert results[0].start_line == 2
    assert results[0].end_line == 5
    assert results[0].complexity == 2


def test_calculate_complexity_async_function():
    source = (
        "async def fetch_user(user_id):\n"
        "    if user_id <= 0:\n"
        "        return None\n"
        "    return {'id': user_id}\n"
    )

    tree = ast.parse(source)
    results = calculate_complexity(tree)

    assert len(results) == 1
    assert results[0].name == "fetch_user"
    assert results[0].start_line == 1
    assert results[0].end_line == 4
    assert results[0].complexity == 2


def test_calculate_complexity_no_functions():
    results = calculate_complexity(ast.parse("x = 10"))

    assert results == []


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

    results = calculate_complexity(analyzer.tree)

    assert len(results) == 1
    assert results[0].name == "check_user"
    assert results[0].complexity == 2