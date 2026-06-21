from preflight.checks.runner import run_checks


def main() -> None:
    raise SystemExit(run_checks())


if __name__ == "__main__":
    main()