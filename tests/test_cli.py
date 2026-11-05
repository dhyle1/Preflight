import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from preflight.analyzers.models import FileAnalysis
from preflight.cli import build_parser, main, print_analysis
from preflight.metrics.models import FunctionInfo, FunctionMetrics


def _function(name, start_line, complexity, length=2) -> FunctionMetrics:
    return FunctionMetrics(
        function=FunctionInfo(name, start_line, start_line + length - 1),
        complexity=complexity,
        length=length,
    )


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


def test_help_explains_running_without_subcommand():
    help_text = " ".join(build_parser().format_help().split())

    assert "without a subcommand to execute Ruff, MyPy and Pytest" in help_text


def test_parser_invalid_command():
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["invalid"])

    assert exc_info.value.code == 2


def test_print_analysis_valid_file(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        function_metrics=[
            _function("process_data", 10, 5, length=11),
            _function("validate_input", 25, 2, length=6),
        ],
        error=None,
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()

    process_line = next(line for line in captured_lines if "process_data" in line)
    validate_line = next(line for line in captured_lines if "validate_input" in line)

    header_line = next(line for line in captured_lines if "LINE" in line)

    assert "example.py" in captured.out
    assert header_line.split() == ["LINE", "CC", "LEN"]
    assert process_line.split()[-3:] == ["10", "5", "11"]
    assert validate_line.split()[-3:] == ["25", "2", "6"]
    assert captured.out.index("process_data") < captured.out.index("validate_input")


def test_print_analysis_unscored_function_shows_dash_and_sorts_last(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        function_metrics=[
            _function("unscored_first", 1, None, length=3),
            _function("scored_low", 5, 1),
            _function("scored_high", 10, 4),
        ],
        error=None,
    )

    print_analysis([file_analysis])
    captured_lines = capsys.readouterr().out.splitlines()

    unscored_line = next(line for line in captured_lines if "unscored_first" in line)
    function_names = [
        line.split()[0]
        for line in captured_lines
        if line.split()[:1] in (["unscored_first"], ["scored_low"], ["scored_high"])
    ]

    assert unscored_line.split()[-3:] == ["1", "-", "3"]
    assert function_names == ["scored_high", "scored_low", "unscored_first"]


def test_print_analysis_summary_skips_unscored_functions(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        function_metrics=[
            _function("unscored", 1, None),
            _function("scored", 5, 1),
        ],
        error=None,
    )

    print_analysis([file_analysis])
    output_lines = capsys.readouterr().out.splitlines()

    assert "Functions:    2" in output_lines
    assert "Most complex: scored (CC 1) at example.py:5" in output_lines


def test_print_analysis_only_unscored_functions(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        function_metrics=[_function("unscored", 1, None)],
        error=None,
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()

    assert "Functions:    1" in captured.out.splitlines()
    assert "Most complex" not in captured.out


def test_print_analysis_file_error(capsys):
    file_analysis = FileAnalysis(
        path=Path("broken.py"),
        function_metrics=[],
        error=SyntaxError("invalid syntax"),
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()

    assert "broken.py" in captured.out
    assert "invalid syntax" in captured.out


def test_print_analysis_no_functions(capsys):
    file_analysis = FileAnalysis(
        path=Path("example.py"),
        function_metrics=[],
        error=None,
    )

    print_analysis([file_analysis])
    captured = capsys.readouterr()

    assert "example.py" in captured.out
    assert "No functions found." in captured.out


def test_print_analysis_multiple_files(capsys):
    first_analysis = FileAnalysis(
        path=Path("main.py"),
        function_metrics=[_function("process_data", 10, 2)],
        error=None,
    )
    second_analysis = FileAnalysis(
        path=Path("utils.py"),
        function_metrics=[_function("format_output", 26, 1)],
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


def test_print_analysis_summary_totals_and_most_complex(capsys):
    results = [
        FileAnalysis(
            path=Path("a.py"),
            function_metrics=[_function("simple", 1, 2)],
            error=None,
        ),
        FileAnalysis(
            path=Path("b.py"),
            function_metrics=[
                _function("low", 1, 1),
                _function("high", 10, 9),
            ],
            error=None,
        ),
    ]

    print_analysis(results)
    output_lines = capsys.readouterr().out.splitlines()

    assert "Files:        2" in output_lines
    assert "Functions:    3" in output_lines
    assert "Errors:       0" in output_lines
    assert "Most complex: high (CC 9) at b.py:10" in output_lines


def test_print_analysis_summary_tie_uses_first_path_and_line(capsys):
    results = [
        FileAnalysis(
            path=Path("b.py"),
            function_metrics=[_function("in_b", 1, 5)],
            error=None,
        ),
        FileAnalysis(
            path=Path("a.py"),
            function_metrics=[
                _function("later", 20, 5),
                _function("earlier", 10, 5),
            ],
            error=None,
        ),
    ]

    print_analysis(results)
    output_lines = capsys.readouterr().out.splitlines()

    assert "Most complex: earlier (CC 5) at a.py:10" in output_lines


def test_print_analysis_summary_counts_errors(capsys):
    results = [
        FileAnalysis(
            path=Path("broken.py"),
            function_metrics=[],
            error=SyntaxError("invalid syntax"),
        ),
        FileAnalysis(
            path=Path("ok.py"),
            function_metrics=[_function("works", 1, 1)],
            error=None,
        ),
    ]

    print_analysis(results)
    output_lines = capsys.readouterr().out.splitlines()

    assert "Files:        2" in output_lines
    assert "Functions:    1" in output_lines
    assert "Errors:       1" in output_lines
    assert "Most complex: works (CC 1) at ok.py:1" in output_lines


def test_print_analysis_summary_no_results(capsys):
    print_analysis([])
    captured = capsys.readouterr()
    output_lines = captured.out.splitlines()

    assert "Files:        0" in output_lines
    assert "Functions:    0" in output_lines
    assert "Errors:       0" in output_lines
    assert "Most complex" not in captured.out


def test_main_no_command(monkeypatch):
    mock_checks = Mock(return_value=0)

    monkeypatch.setattr(sys, "argv", ["preflight"])
    monkeypatch.setattr("preflight.cli.run_checks", mock_checks)

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    mock_checks.assert_called_once_with()


def test_main_analyze_command(monkeypatch):
    mock_analyze = Mock(return_value=[])
    mock_print = Mock()

    monkeypatch.setattr(sys, "argv", ["preflight", "analyze", "src/"])
    monkeypatch.setattr("preflight.cli.analyze_directory", mock_analyze)
    monkeypatch.setattr("preflight.cli.print_analysis", mock_print)

    main()

    mock_analyze.assert_called_once_with(Path("src/"))
    mock_print.assert_called_once_with([])


def test_main_analyze_nonexistent_dir(monkeypatch):
    mock_analyze = Mock(
        side_effect=NotADirectoryError("Invalid directory: nonexistent")
    )

    monkeypatch.setattr(sys, "argv", ["preflight", "analyze", "nonexistent/"])
    monkeypatch.setattr("preflight.cli.analyze_directory", mock_analyze)

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == "Error: Invalid directory: nonexistent"
