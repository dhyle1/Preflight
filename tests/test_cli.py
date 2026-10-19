from pathlib import Path

import pytest

from preflight.cli import build_parser


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
