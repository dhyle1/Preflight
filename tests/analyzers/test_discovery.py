from pathlib import Path

import pytest

from preflight.analyzers.discovery import discover_python_files


def test_discover_files_in_root(tmp_path: Path):
    main = tmp_path / "main.py"
    utils = tmp_path / "utils.py"
    readme = tmp_path / "readme.md"

    main.write_text("")
    utils.write_text("")
    readme.write_text("")

    result = discover_python_files(tmp_path)

    assert result == [
        tmp_path / "main.py", 
        tmp_path / "utils.py",
        ]


def test_discover_nested_files(tmp_path: Path):
    directory = tmp_path / "main"
    directory.mkdir()

    nested = directory / "nested.py"
    nested.write_text("")

    result = discover_python_files(tmp_path)

    assert result == [nested]


def test_discover_excluded_dirs(tmp_path: Path):
    excluded = tmp_path / ".venv"
    excluded.mkdir()

    (excluded / "library.py").write_text("")

    valid = tmp_path / "main.py"
    valid.write_text("")

    result = discover_python_files(tmp_path)

    assert result == [valid]


def test_discover_empty_directory(tmp_path: Path):
    directory = tmp_path / "main"
    directory.mkdir()

    result = discover_python_files(tmp_path)

    assert result == []


def test_discover_invalid_root(tmp_path: Path):
    invalid = tmp_path / "nonexistent"

    with pytest.raises(NotADirectoryError):
        discover_python_files(invalid)


def test_discover_sorted_files(tmp_path: Path):
    z = tmp_path / "z.py"
    a = tmp_path / "a.py"
    m = tmp_path / "m.py"

    z.write_text("")
    m.write_text("")
    a.write_text("")

    result = discover_python_files(tmp_path)

    assert result == [a, m, z]
