"""
Initialization of belief base
"""

import sympy
from DPLL import DPLL
# Define symbols
A, B, C, D, E, F = sympy.symbols('A B C D E F')

expr1 = sympy.Equivalent(A,(C | E))
expr2 = sympy.Implies(E,D)
expr3 = sympy.Implies((B & F),sympy.Not(C))
expr4 = sympy.Implies(E,C)
expr5 = C >> F
expr6 = C >> B

pre_KB = [expr1,expr2,expr3,expr4,expr5,expr6]
# convert sentence into cnf 
KB = [sympy.to_cnf(expr) for expr in pre_KB]

symbols = [A, B, C, D, E, F]

# define test expression for AGM postulates tests
test_expr0 = sympy.And(A,B)
test_expr1 = sympy.And(B,A)
test_expr2 = sympy.Equivalent(A,(E | C))
test_expr3 = F >> C
test_expr4 = sympy.Not(F) >> sympy.Not(C)