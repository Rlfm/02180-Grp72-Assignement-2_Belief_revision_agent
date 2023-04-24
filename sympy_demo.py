import sympy
from DPLL import DPLL
# Define some symbols
A, B, C, D, E, F = sympy.symbols('A B C D E F')

expr1 = sympy.Equivalent(A,(C | E))
expr2 = sympy.Implies(E,D)
expr3 = sympy.Implies((B & F),sympy.Not(C))
expr4 = sympy.Implies(E,C)
expr5 = C >> F
expr6 = C >> B 

pre_KB = [expr1,expr2,expr3,expr4,expr5,expr6]
KB = [sympy.to_cnf(expr) for expr in pre_KB]

symbols = [A, B, C, D, E, F]
# Print the expressions
for i,expr in enumerate(KB):
    print(f"Expression {i} {expr}")

print(f"original {KB=}")

DPLL_return = DPLL(KB,symbols)

print(f"{DPLL(KB,symbols)=}")

for i,expr in enumerate(KB):
    print(f"Expression {i} {expr} -> with DPLL proposed model: {expr.subs(DPLL_return[1])}")s