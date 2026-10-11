import ast
from pathlib import Path


class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.tree: ast.Module | None = None
        self.functions: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
        self.classes: list[ast.ClassDef] = []

    def analyze(self) -> None:
        source = self.path.read_text()
        self.tree = ast.parse(source)
        self.visit(self.tree)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions.append(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.functions.append(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.classes.append(node)
        self.generic_visit(node)

