import sympy
from sympy_demo import KB, symbols, expr1
from DPLL import DPLL
from itertools import chain, combinations, product
from entrenchment import reorder_expressions


def tautology(s, assignments):
    lst = []
    for a in assignments:
        if s.subs(a) == True:
            lst.append(s)
    if len(lst) == len(assignments):
        return True

def entrenchment_contract(l, p, symbols):
    
    tautologies_ = []
    contraction = []

    _KB = reorder_expressions(l)
    p_entrench = _KB.index(p)

    cnf = tuple(_KB)

    assignments = [dict(zip(symbols, values)) for values in product([True, False], repeat=len(symbols))]

    for s in _KB:
        if tautology(s, assignments):
            contraction.append(s)

    for s in _KB:
        if s not in contraction:
           q = sympy.to_cnf(_KB[p_entrench]| s)
           print(_KB)
           print(q)
           if q in _KB and _KB.index(q) < p_entrench: 
               contraction.append(q)

    print(contraction)


entrenchment_contract(KB, expr1, symbols)


