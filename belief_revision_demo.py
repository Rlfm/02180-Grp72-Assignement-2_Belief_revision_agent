"""
Functions for calling belief revision
"""

import sympy
from DPLL import DPLL
from contraction import contract, AGM_Rationality_Postulates_for_contraction
from revision import expand, AGM_Rationality_Postulates_for_expansion
from belief_base import KB, symbols, expr1, test_expr0, test_expr1, test_expr2

def showKB():
    """
    Displays the beliefs base, and checks satisfiability of beliefs.
    """

    DPLL_return = DPLL(KB,symbols)

    print(f"{DPLL(KB,symbols)=}")
    
    print("\nTest satisfiability of beliefs: ")
    for i,expr in enumerate(KB):
        print(f"Expression {i} {expr} -> with DPLL proposed model: {expr.subs(DPLL_return[1])}")

    print(f"\nInitial {KB=}")

def contractKB(KB, s) -> list:
    """
    Function for calling contraction of belief base KB, by sentence s. 
    """
    return contract(KB, s)
    

def expandKB(KB, s) -> list: 
    """
    Function for calling revision of belief base KB, by expansion by sentence s. 
    """
    return expand(KB, s)


showKB()
print()
print(f"Expand KB by sentence s = {test_expr0}")
expandedKB = expandKB(KB, test_expr0)
print(expandedKB)
AGM_Rationality_Postulates_for_expansion(KB, test_expr0, test_expr1, expandedKB)
print()

print(f"Contract KB by sentence s = {expr1}")
contractedKB = contractKB(KB, expr1)
print(contractedKB)

AGM_Rationality_Postulates_for_contraction(KB, expr1, test_expr2, contractedKB)

