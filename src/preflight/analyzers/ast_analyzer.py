import ast
import tokenize
from pathlib import Path

from preflight.metrics.models import FunctionInfo


class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.tree: ast.Module | None = None
        self.functions: list[FunctionInfo] = []
        self.classes: list[ast.ClassDef] = []
        self.error: Exception | None = None
        self._scope: list[str] = []

    def analyze(self) -> None:
        try:
            with tokenize.open(self.path) as file:
                source = file.read()

            self.tree = ast.parse(source)
            self.visit(self.tree)

        except(SyntaxError, UnicodeDecodeError, OSError) as error:
            self.error = error

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.classes.append(node)
        self._visit_in_scope(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        name = ".".join([*self._scope, node.name])
        end_line = node.end_lineno or node.lineno  # typed as optional
        self.functions.append(FunctionInfo(name, node.lineno, end_line))

        self._visit_in_scope(node)

    def _visit_in_scope(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    ) -> None:
        self._scope.append(node.name)
        self.generic_visit(node)
        self._scope.pop()
