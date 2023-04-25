import sympy
from sympy_demo import KB, expr1, symbols
from DPLL import DPLL
from entrenchment import reorder_expressions
from itertools import chain, combinations, product

#def meet(K):
 #   return sympy.And(*K)

ex1 = expr1
""""
function, which given a set of belief bases K, and a sentence s 
returns a set K' containing all k in K which do not imply s

"""
def _remove_implications(K, s):
    s = [sympy.Not(s)]
    candidates = []
    for k in K:
        #F = [meet(k + s)]
        F = k + s
        SAT, result = DPLL(F, symbols)
        if SAT:
            candidates.append(k)
    return candidates


def powerset(A, r):
    # Compute the powerset of A 
    return [list(x) for x in chain.from_iterable(combinations(A, r) for r in range(r))]
        
def intersection(r1, r2):
    # returns intersection of two lists 
    r3 = [value for value in r1 if value in r2]
    return r3

def partial_meet(KB, s):
    # Limit removals
    removals = 0

    # empty list to store candidates for remainder set
    candidates = []

    # while no candidstes are found, increase removals from belief base 
    while (len(candidates) == 0): 
        removals += 1

        # compute powerset of KB with removals
        p = powerset(KB, len(KB) - removals)

        candidates = (_remove_implications(p, s))
    
    # Remove list in candidates that are strictly included in other list in candidates, to find remainders 
    remainders = [S for i, S in enumerate(candidates) if not any(set(S).issubset(set(T)) and set(S)!=set(T) for T in candidates[i+1:])]

    # compute intersection of first two remainders
    contraction = intersection(remainders[0], remainders[1])

    return contraction

print(KB)
print(partial_meet(KB, ex1))
    
    

 