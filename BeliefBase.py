"""
Functions for calling beliefrevision
"""

import sympy
from DPLL import DPLL
from contraction import contract
from revision import expand
from sympy_demo import KB, symbols, test_expr, expr1


def showKB():
    # Print the expressions
    for i,expr in enumerate(KB):
        print(f"Expression {i} {expr}")

    print(f"original {KB=}")

    DPLL_return = DPLL(KB,symbols)

    print(f"{DPLL(KB,symbols)=}")

    for i,expr in enumerate(KB):
        print(f"Expression {i} {expr} -> with DPLL proposed model: {expr.subs(DPLL_return[1])}")

def contractKB(KB, s):
    print(f"{KB=}")
    print(contract(KB, s))
    

def expandKB(KB, s):
    print(f"{KB= }")
    print(expand(KB, s))


print(f"Expand KB by sentence s = {test_expr}")
expandKB(KB, test_expr)

print(f"Contract KB by sentence s = {expr1}")
contractKB(KB, expr1)
