import ast

from radon.complexity import add_inner_blocks, cc_visit_ast
from radon.visitors import Function


def calculate_complexity(tree: ast.AST) -> dict[int, int]:
    radon_functions = add_inner_blocks(cc_visit_ast(tree))

    return {
        function.lineno: function.complexity
        for function in radon_functions
        if isinstance(function, Function)
    }
