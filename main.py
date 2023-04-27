import sympy
from sympy import FiniteSet
from DPLL import DPLL
import revision

# Define some symbols
A, B, C, D, E, F = sympy.symbols('A B C D E F')

expr1 = sympy.Implies(A,B)
expr2 = sympy.Not(B)
expr3 = A
expr4 = sympy.And(C, A)
expr5 = B
expr6 = C
expr7 = sympy.Not(sympy.Or(C, A))

add_expr_1 = sympy.to_cnf(expr7)

pre_KB = [expr3, expr5, expr6]
KB = {sympy.to_cnf(expr) for expr in pre_KB}
new_KB = FiniteSet(*KB)
symbols = new_KB.free_symbols

current_minimal_state = revision.find_minimal_state(new_KB)
print("Before revision")
print(new_KB)
print(current_minimal_state)
new_belief = add_expr_1
symbols = symbols | new_belief.free_symbols
symbols = [i for i in symbols]
KB_1 = revision.adding_new(new_KB, new_belief)
test_KB = {k for k in KB_1}
check_inconsistency = DPLL(test_KB,symbols)
print(check_inconsistency)
if check_inconsistency[0]==False:
    KB_1, current_minimal_state = revision.revision(new_KB, new_belief, current_minimal_state)
    print("After revision")
    print(KB_1)
    print(current_minimal_state)
else:
    KB_1 = revision.adding_new(new_KB, new_belief)
    current_minimal_state = revision.find_minimal_state(KB_1)
    print("After revision")
    print(KB_1)
    print(current_minimal_state)

