from pathlib import Path

import pytest

from preflight.analyzers.models import FileAnalysis
from preflight.cli import build_parser, print_analysis
from preflight.metrics.models import FunctionComplexity


def test_parser_no_command():
    parser = build_parser()
    args = parser.parse_args([])

    assert args.command is None


def test_parser_analyse_default_path():
    parser = build_parser()
    args = parser.parse_args(["analyze"])

    assert args.command == "analyze"
    assert args.path == Path(".")


def test_parser_analyze_custom_path():
    parser = build_parser()
    args = parser.parse_args(["analyze", "src/"])

    assert args.command == "analyze"
    assert args.path == Path("src")


def test_parser_invalid_command():
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["invalid"])

    assert exc_info.value.code == 2


def test_print_analysis_valid_file(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        complexity_metrics=[
            FunctionComplexity(
                name="process_data",
                start_line=10,
                end_line=20,
                complexity=5,
            ),
            FunctionComplexity(
                name="validate_input",
                start_line=25,
                end_line=30,
                complexity=2,
            ),
        ],
        error=None,
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()

    process_line = next(line for line in captured_lines if "process_data" in line)
    validate_line = next(line for line in captured_lines if "validate_input" in line)

    assert "example.py" in captured.out
    assert process_line.split()[-2:] == ["10", "5"]
    assert validate_line.split()[-2:] == ["25", "2"]
    assert captured.out.index("process_data") < captured.out.index("validate_input")


def test_print_analysis_file_error(capsys):
    file_analysis = FileAnalysis(
        path=Path("broken.py"),
        complexity_metrics=[],
        error=SyntaxError("invalid syntax"),
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()

    assert "broken.py" in captured.out
    assert "invalid syntax" in captured.out


def test_print_analysis_no_functions(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        complexity_metrics=[],
        error=None,
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()

    assert "example.py" in captured.out
    assert "No functions found." in captured.out


def test_print_analysis_multiple_files(capsys):
    first_analysis = FileAnalysis(
        path=Path("main.py"),
        complexity_metrics=[
            FunctionComplexity(
                name="process_data",
                start_line=10,
                end_line=20,
                complexity=2,
            ),
        ],
        error=None,
    )
    second_analysis = FileAnalysis(
        path=Path("utils.py"),
        complexity_metrics=[
            FunctionComplexity(
                name="format_output",
                start_line=26,
                end_line=35,
                complexity=1,
            ),
        ],
        error=None,
    )

    print_analysis([first_analysis, second_analysis])
    captured = capsys.readouterr()

    assert (
        captured.out.index("main.py")
        < captured.out.index("process_data")
        < captured.out.index("utils.py")
        < captured.out.index("format_output")
    )
