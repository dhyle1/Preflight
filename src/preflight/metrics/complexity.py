import ast

from radon.complexity import add_inner_blocks, cc_visit_ast
from radon.visitors import Function

from preflight.metrics.models import FunctionComplexity


def calculate_complexity(tree: ast.AST) -> list[FunctionComplexity]:
    radon_functions = add_inner_blocks(cc_visit_ast(tree))
    complexity_metrics: list[FunctionComplexity] = []

    for function in radon_functions:
        if not isinstance(function, Function):
            continue

        scoped_name = (
            f"{function.classname}.{function.name}"
            if function.classname
            else function.name
        )
        
        complexity_metrics.append(
            FunctionComplexity(
                name=scoped_name,
                start_line=function.lineno,
                end_line=function.endline,
                complexity=function.complexity,
            )
        )

    return complexity_metrics