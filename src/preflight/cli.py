import argparse
from pathlib import Path

from preflight.analyzers.directory_analyzer import analyze_directory
from preflight.analyzers.models import FileAnalysis
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


def print_analysis(results: list[FileAnalysis]) -> None:
    print("\nPreflight Analysis")
    print("-" * 65)

    name_width = max(
        (
            len(metric.name)
            for file_analysis in results
            for metric in file_analysis.complexity_metrics
        ),
        default=0,
    )

    for file_analysis in results:
        print(f"\n{file_analysis.path}")

        if file_analysis.error is not None:
            print(f"  Error: {file_analysis.error}")
            continue

        if not file_analysis.complexity_metrics:
            print("  No functions found.")
            continue

        metrics = sorted(
            file_analysis.complexity_metrics,
            key=lambda metric: (-metric.complexity, metric.start_line),
        )

        print(f"  {'':<{name_width}}  {'LINE':>4}  {'CC':>4}")

        for metric in metrics:
            print(
                f"  {metric.name:<{name_width}}  "
                f"{metric.start_line:>4}  "
                f"{metric.complexity:>4}"
            )

    print()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        try:
            directory_analysis = analyze_directory(args.path)
            print_analysis(directory_analysis)
        except(NotADirectoryError) as exc:
            raise SystemExit(f"Error: {exc}") from None
        
    elif args.command is None:
        raise SystemExit(run_checks())


if __name__ == "__main__":
    main()
