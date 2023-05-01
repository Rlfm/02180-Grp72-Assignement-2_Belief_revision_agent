import sympy
from sympy import FiniteSet
from DPLL import DPLL
import revision

# Define sympy symbols
A, B, C, D, E, F = sympy.symbols('A B C D E F')

# Belief statements
expr1 = sympy.Implies(A,B)
expr2 = sympy.Not(B)
expr3 = A
expr4 = sympy.And(C, A)
expr5 = B
expr6 = C
expr7 = sympy.Not(sympy.Or(C, A))

# New belief which needs to be added to the agent beliefs
new_belief = sympy.to_cnf(expr7)

# Initializing knowledge base of the agent and minimal state
pre_KB = [expr3, expr5, expr6]
KB = {sympy.to_cnf(expr) for expr in pre_KB}
agent_KB = FiniteSet(*KB)
symbols = agent_KB.free_symbols
current_minimal_state = revision.find_minimal_state(agent_KB)
print("Before revision")
print(agent_KB)
print(current_minimal_state)

# The below lines of code performs revision to the Agent beliefs according to the new coming belief
symbols = symbols | new_belief.free_symbols
symbols = [i for i in symbols]
KB_1 = revision.adding_new(agent_KB, new_belief)
test_KB = {k for k in KB_1}
check_inconsistency = DPLL(test_KB,symbols)
if check_inconsistency[0]==False:                                       # If the coming belief is NOT consistent with the agent beliefs
    KB_1, current_minimal_state = revision.revision(agent_KB, new_belief, current_minimal_state)
    print("After revision")
    print(KB_1)
    print(current_minimal_state)
else:                                                                   # If the coming belief is consistent with the agent beliefs
    KB_1 = revision.adding_new(agent_KB, new_belief)
    current_minimal_state = revision.find_minimal_state(KB_1)
    print("After revision")
    print(KB_1)
    print(current_minimal_state)
