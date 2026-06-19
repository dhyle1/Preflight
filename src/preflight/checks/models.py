from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    exit_code: str

    @property
    def passed(self) -> bool:
        return self.exit_code == 0