from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Finding:
    file: Path
    line: int | None
    message: str


@dataclass
class CheckResult:
    name: str
    exit_code: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.exit_code == 0