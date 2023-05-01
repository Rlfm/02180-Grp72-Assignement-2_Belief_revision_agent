from sympy import to_cnf, to_dnf, Not
from sympy_demo import KB, expr1, symbols
from DPLL import DPLL
from entrenchment import reorder_expressions
from itertools import chain, combinations


def AGM_Rationality_Postulates_for_contraction(KB, expr, KB_post_contraction):
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
    assert KB_post_contraction == contract(KB, expr2), "The outcomes of contracting with equivalent sentences are not equal"



def remove_implications(K, s):
    """
    function, which given a set of belief bases K, and a sentence s 
    returns a set K' containing all k in K which do not imply s
    """

    if len(K) == 0:
        return []
    
    s = [Not(s)]
    candidates = []
    for k in K:
        #F = [meet(k + s)]
        F = k + s
        SAT, result = DPLL(F, symbols)
        if SAT:
            candidates.append(k)
    return candidates


def powerset(A, r):
    """
    returns powerset of set A of lenght r.
    """
    return [list(x) for x in chain.from_iterable(combinations(A, r) for r in range(r))]
        
def intersection(r1, r2):
    """
    Returns intersection of two lists.
    """
    r3 = [value for value in r1 if value in r2]
    return r3

def selection_function(KB, remainders):
    """
    Selection function, returns the two best remainders based on entrencment ordering.
    """

    # reorder the beliefs in base, from least to most entrenched
    # the score of each belief correspond to its index in the reordered belief base
    entrenchment_order = reorder_expressions(KB)
    entrenchment_order.reverse()

    scores = []
    for r in remainders:
        # r_max_score; the score of most entreched belief contained in r 
        r_max = max([entrenchment_order.index(s) for s in r]) if r else 0
        # r_avg_score; avareage of scores of all beliefs in r
        r_avg = sum([entrenchment_order.index(s) for s in r]) / len(r) if r else 0

        # total score of r, is a weitghted sum  of r_max_score and r_avg_score
        score = 0.6 * r_max + 0.4 * r_avg 
        scores.append((r, score))
    
    # the remainders er sorted based scores
    scores.sort(key=lambda x: x[1], reverse=True)

    # two highest scoring remainders are returned
    best_remainders = [r for r, _ in scores[:2]]
    return best_remainders

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def contract(KB, s):
    """
    Partial meet conatraction on belief base. 
    Returns contraction by a sentence s, of belief base KB. 
    """

    s = to_cnf(s)

    KB_copy = KB.copy()

    if not s in KB :
        return KB
    
    _s = KB_copy.index(s)
    KB_copy[_s:_s+1] = []

    if len(KB_copy) == 1:
        return remove_implications(KB_copy, s)
    
    # Limit removals
    removals = 1

    # empty list to store candidates for remainder set
    candidates = []

    candidates = remove_implications([KB_copy], s)

    # while no candidstes are found, increase removals from belief base 
    while (len(candidates) == 0): 

        # compute powerset of KB with removals
        p = powerset(KB_copy, len(KB) - removals)
        
        removals += 1
        
        candidates = (remove_implications(p, s))
    
    # Remove list in candidates that are strictly included in other list in candidates, to find remainders 
    remainders = [S for i, S in enumerate(candidates) if not any(set(S).issubset(set(T)) and set(S)!=set(T) for T in candidates[i+1:])]

    # selection function returns two remainders for contraction
    best_remainders = selection_function(KB, remainders)

    # The contraction is the intersection of the selected remainders
    contraction = list(set(best_remainders[0]).intersection(*best_remainders[1:]))

    AGM_Rationality_Postulates_for_contraction(KB, s, contraction)

    return contraction

        
    

 