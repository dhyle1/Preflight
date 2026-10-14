from pathlib import Path

from preflight.analyzers.discovery import discover_python_files
from preflight.analyzers.file_analyzer import analyze_file
from preflight.analyzers.models import FileAnalysis


def analyze_directory(root: Path) -> list[FileAnalysis]:
    files = discover_python_files(root)
    directory_analysis: list[FileAnalysis] = []

    for file in files:
        file_analysis = analyze_file(file)
        directory_analysis.append(file_analysis)

    return directory_analysis
