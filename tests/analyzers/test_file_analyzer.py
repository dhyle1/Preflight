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
    assert len(result.function_metrics) == 1

    metric = result.function_metrics[0]
    assert metric.function.name == "check_user"
    assert metric.complexity == 2
    assert metric.length == 4


def test_analyze_file_length_counts_blank_lines_and_docstring(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
        "@decorator\n"
        "def documented():\n"
        '    """Docstring."""\n'
        "\n"
        "    return 1\n"
        "    # trailing comment\n"
    )

    metric = analyze_file(file).function_metrics[0]

    assert metric.function.start_line == 2
    assert metric.length == 4


def test_analyze_file_length_counts_multiline_signature(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
        "def long_signature(\n"
        "    first,\n"
        "    second,\n"
        "):\n"
        "    return first\n"
    )

    metric = analyze_file(file).function_metrics[0]

    assert metric.length == 5


def test_analyze_file_duplicate_names_stay_separate(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text(
        "if flag:\n"
        "    def choose(x):\n"
        "        if x:\n"
        "            return 1\n"
        "        return 2\n"
        "else:\n"
        "    def choose(x):\n"
        "        return 3\n"
    )

    metrics = analyze_file(file).function_metrics

    assert [metric.function.name for metric in metrics] == ["choose", "choose"]
    assert [metric.complexity for metric in metrics] == [2, 1]
    assert [metric.length for metric in metrics] == [4, 2]


def test_analyze_file_local_class_method_has_length_without_complexity(
    tmp_path: Path,
):
    file = tmp_path / "example.py"
    file.write_text(
        "def outer():\n"
        "    class Local:\n"
        "        def method(self):\n"
        "            return 1\n"
    )

    metrics = analyze_file(file).function_metrics
    outer, method = metrics

    assert outer.function.name == "outer"
    assert outer.complexity == 1
    assert outer.length == 4

    assert method.function.name == "outer.Local.method"
    assert method.complexity is None
    assert method.length == 2


def test_analyze_file_invalid_syntax(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("def broken(:\n    pass\n")

    result = analyze_file(file)

    assert isinstance(result.error, SyntaxError)
    assert result.function_metrics == []


def test_analyze_file_no_functions(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("x = 42\n")

    result = analyze_file(file)

    assert result.path == file
    assert result.error is None
    assert result.function_metrics == []


def test_analyze_file_nonexistent_file(tmp_path: Path):
    file = tmp_path / "nonexistent.py"

    result = analyze_file(file)

    assert result.path == file
    assert isinstance(result.error, FileNotFoundError)
    assert result.function_metrics == []


def test_analyze_latin_encoding(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_bytes(
        '# coding: latin-1\nmessage = "café"\n'.encode("latin-1")
    )

    result = analyze_file(file)

    assert result.error is None
    assert result.function_metrics == []
