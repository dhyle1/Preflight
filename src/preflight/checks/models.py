from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    exit_code: int

    @property
    def passed(self) -> bool:
        return self.exit_code == 0