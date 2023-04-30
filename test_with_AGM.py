from sympy import to_cnf, to_dnf, Not
from DPLL import DPLL
from itertools import chain, combinations, product
from revision import contraction_using_plausibility_order, adding_new


def AGM_Rationality_Postulates_for_contraction(KB, expr, KB_post_contraction, current_minimal_state):
    """
    functions that assess that AGM postulates are respected for the present contraction 
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

def AGM_Rationality_Postulates_for_expansion(KB, expr, KB_post_expansion):
    """
    functions that asses that AGM postulates are respected for the present expansion. 
    """
    # Sucess 
    assert expr not in KB_post_expansion, f"{expr} is still part of KB after expansion"

    # Inclusion
    
    assert all(x in KB.copy().append(expr) for x in KB_post_expansion), "KB after revision is not a subset of original KB after expansion"

    # Vacuity
    if expr not in KB:
        assert KB == KB_post_expansion, "KB was modified but {expr} wasn't in KB"

    # Consistency
    if consistensy(expr):
        assert consistensy(KB_post_expansion), f"{expr} is consisten but, KB after expansion is not"
    
    # Extensionality
    expr2 = to_dnf(expr)
    assert KB_post_expansion == adding_new(KB, expr2), "The outcomes of contracting with equivalent sentences are not equal"