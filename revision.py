from contraction import contract
from sympy import to_cnf, to_dnf, Not
from sympy_demo import KB, F, C
from DPLL import DPLL

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
    assert KB_post_expansion == expand(KB, expr2), "The outcomes of contracting with equivalent sentences are not equal"

def consistensy(set_):
    """
    Returns if a set of beliefs is consistent.
    """
    result, list = DPLL(set_)
    return result

def expand(KB, s):
    """
    Expasion of beliefs, by a sentence s.
    """
    s = to_cnf(s)
    neg_s = to_cnf(Not(s))

    if s not in KB: 
        KB = contract(KB, neg_s)
        KB.append(s)
        return KB

    return KB

if __name__ =='__main__':
    expr = F >> C
    print(expand(KB, expr))