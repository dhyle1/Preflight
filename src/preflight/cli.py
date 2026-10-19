import argparse
from pathlib import Path

from preflight.analyzers.directory_analyzer import analyze_directory
from preflight.checks.runner import run_checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze Python projects with Preflight"
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze Python files",
    )

    analyze_parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path("."),
        metavar="DIR",
        help="Directory to analyze (default: current directory)",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        directory_analysis = analyze_directory(args.path)
    elif args.command is None:
        raise SystemExit(run_checks())


if __name__ == "__main__":
    main()