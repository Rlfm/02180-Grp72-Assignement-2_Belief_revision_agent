import sympy
from sympy import FiniteSet
from DPLL import DPLL
# Define some symbols
A, B, C, D, E, F = sympy.symbols('A B C D E F')

#expr1 = sympy.Equivalent(A,(C | E))
#expr2 = sympy.Implies(E,D)
#expr3 = sympy.Implies((B & F),sympy.Not(C))
#expr4 = sympy.Implies(E,C)
#expr5 = C >> F 
#expr6 = C >> B 

expr1 = sympy.Implies(A,B)
expr2 = sympy.Not(B)
expr3 = A
expr4 = sympy.And(C, A)
expr5 = C

#pre_KB = [expr1,expr2,expr3,expr4,expr5,expr6]
pre_KB = [expr1,expr2,expr3, expr4]
test_KB = [expr4]
KB = {sympy.to_cnf(expr) for expr in pre_KB}
new_KB = FiniteSet(*KB)
KB2 = new_KB.append(sympy.to_cnf(expr5))

symbols = new_KB.free_symbols
KB1 = new_KB.subs({C: True, A: False})
aaa = len(KB1.args)
ss = {C: True, A: False}
other_s = {i: True for i in symbols}
new = ss | other_s
new2 = other_s | ss
symbols = [C, A]
#symbols = new_KB.free_symbols
#symbols.remove(C)
#symbols.add(D)
#b = expr4.subs({C: True, A: False})
a = A.assumptions0

# Print the expressions
for i,expr in enumerate(KB):
    print(f"Expression {i} {expr}")
    #l = expr.args[1]

print(f"original {KB=}")
#print(f"{DPLL(KB,symbols)=}")
#k = DPLL(KB,symbols)
c = DPLL(test_KB,symbols)
k = c[1].keys()
for k1 in k:
    k2 = k1
l = type(k)
print (c)