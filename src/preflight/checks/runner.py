import subprocess


def run_ruff() -> None:
    subprocess.run(["ruff", "check", "."])


def run_checks() -> None:
    print("Running checks...")
    run_ruff()