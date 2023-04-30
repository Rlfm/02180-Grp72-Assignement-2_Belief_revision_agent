from sympy import to_cnf, to_dnf, Not
from sympy_demo import KB, expr1, symbols
from DPLL import DPLL
from entrenchment import reorder_expressions
from itertools import chain, combinations, product
from revision import contraction_using_plausibility_order


def AGM_Rationality_Postulates_for_contraction(KB, expr, KB_post_contraction, current_minimal_state):
    """
    functions that asses that AGM postulates are respected for the present contraction 
    """
    expr = to_cnf(expr)
    # Success
    assert expr not in KB_post_contraction, f"{expr} is still part of KB after contraction"

    # Inclusion 
    assert len([x for x in KB_post_contraction if x in KB]) == len(KB_post_contraction), "KB after contraction is not a subset of original KB"

    # Vacuity 
    if expr not in KB:
        assert KB == KB_post_contraction, f"KB was modified but {expr} wasn't in KB"

    # Extensionality
    expr2 = to_dnf(expr)
    X,Y = contraction_using_plausibility_order(KB, expr2, current_minimal_state)
    assert KB_post_contraction == X, "The outcomes of contracting with equivalent sentences are not equal"
