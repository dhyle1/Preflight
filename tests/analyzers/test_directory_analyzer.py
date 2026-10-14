from pathlib import Path

from preflight.analyzers.directory_analyzer import analyze_directory


def test_analyze_directory_multiple_valid_files(tmp_path: Path):
    (tmp_path / "first.py").write_text("def foo():\n    pass\n")
    (tmp_path / "second.py").write_text("def bar():\n    pass\n")

    results = analyze_directory(tmp_path)

    assert len(results) == 2
    assert [result.path.name for result in results] == ["first.py", "second.py"]
    assert all(result.error is None for result in results)
    assert all(len(result.complexity_metrics) == 1 for result in results)


def test_analyze_directory_valid_and_invalid_files(tmp_path: Path):
    (tmp_path / "valid.py").write_text("def foo():\n    pass\n")
    (tmp_path / "invalid.py").write_text("def broken(:\n    pass\n")

    results = analyze_directory(tmp_path)

    assert len(results) == 2

    results_by_name = {result.path.name: result for result in results}

    assert isinstance(results_by_name["invalid.py"].error, SyntaxError)
    assert results_by_name["invalid.py"].complexity_metrics == []

    assert results_by_name["valid.py"].error is None
    assert len(results_by_name["valid.py"].complexity_metrics) == 1


def test_analyze_directory_empty_directory(tmp_path: Path):
    results = analyze_directory(tmp_path)

    assert results == []
