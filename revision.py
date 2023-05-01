from contraction import contract
from sympy import to_cnf, Not
from belief_base import symbols
from DPLL import DPLL

def AGM_Rationality_Postulates_for_expansion(KB, expr, test_expr, KB_post_expansion):
    """
    functions that asses that AGM postulates are respected for the present expansion. 
    """
    # Sucess 
    assert expr not in KB_post_expansion, f"{expr} is still part of KB after expansion"

    # Inclusion
    
    assert all(x in KB for x in KB_post_expansion), f"KB after revision is not a subset of original KB {KB} after expansion"

    # Vacuity
    if Not(expr) not in KB:
        assert KB == KB_post_expansion, "KB was modified but neg{expr} wasn't in KB"

    # Consistency
    _expr = [to_cnf(expr)]
    if consistensy(_expr):
        assert consistensy(KB_post_expansion), f"{expr} is consisten but, KB after expansion {KB_post_expansion} is not"
    
    # Extensionality
    assert KB_post_expansion == expand(KB, test_expr), "The outcomes of contracting with equivalent sentences are not equal"

def consistensy(set_):
    """
    Returns if a set of beliefs is consistent.
    """
    result, list = DPLL(set_, symbols)
    return result

def expand(KB, s):
    """
    Expasion of beliefs, by a sentence s.
    """
    s = to_cnf(s)
    neg_s = to_cnf(Not(s))

    if s not in KB: 
        contracted_KB = contract(KB, neg_s)
        contracted_KB.append(s)
        return KB

    return KB
