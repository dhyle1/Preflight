import os
from pathlib import Path

EXCLUDED_DIRS = {
    # Version control
    ".git",

    # Virtual environments
    ".venv",
    "venv",
    "env",
    ".env",

    # Python caches
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".nox",

    # Build artifacts
    "build",
    "dist",

    # Other tooling
    ".idea",
    ".vscode",
    "node_modules",
}


def discover_python_files(root: Path) -> list[Path]:
    if not root.is_dir():
        raise NotADirectoryError(f"Invalid directory: {root}")

    files: list[Path] = []

    for current_dir, dirs, filenames in os.walk(root, followlinks=False):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in filenames:
            if filename.endswith(".py"):
                files.append(Path(current_dir) / filename)

    return sorted(files)
