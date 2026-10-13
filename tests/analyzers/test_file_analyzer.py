from pathlib import Path

from preflight.analyzers.file_analyzer import analyze_file


def test_analyze_file_valid_python(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
        "def check_user(user):\n"
        "    if user.active:\n"
        "        return True\n"
        "    return False\n"
    )

    result = analyze_file(file)

    assert result.path == file
    assert result.error is None
    assert len(result.complexity_metrics) == 1

    metric = result.complexity_metrics[0]
    assert metric.name == "check_user"
    assert metric.complexity == 2


def test_analyze_file_invalid_syntax(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("def broken(:\n    pass\n")

    result = analyze_file(file)

    assert isinstance(result.error, SyntaxError)
    assert result.complexity_metrics == []


def test_analyze_file_no_functions(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("x = 42\n")

    result = analyze_file(file)

    assert result.path == file
    assert result.error is None
    assert result.complexity_metrics == []


def test_analyze_file_nonexistent_file(tmp_path: Path):
    file = tmp_path / "nonexistent.py"

    result = analyze_file(file)

    assert result.path == file
    assert isinstance(result.error, FileNotFoundError)
    assert result.complexity_metrics == []