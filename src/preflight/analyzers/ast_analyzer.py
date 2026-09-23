import ast
from pathlib import Path

from preflight.checks.models import Finding


class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.findings: list[Finding] = []

    def analyze(self) -> list[Finding]:
        source = self.path.read_text()
        tree = ast.parse(source)

        self.visit(tree)

        return self.findings