import sympy
# Define some symbols
A, B, C, D = sympy.symbols('A B C D')

# Define some logical expressions
expr1 = (A|B) & (A|C)
expr2 = sympy.Or(expr1,C)
expr3 = B >> (A | D)

zi_expr = (expr1 ^C) | expr3

# Print the expressions
print("Expression 1:", expr1)
print("Expression 2:", expr2)
print("Expression 3:", expr3)

# Evaluate the expressions for some truth values
truth_values = {
    A: True,
    B: False,
    C: True
}
"""
print("Expression 1 evaluates to:", expr1.subs(truth_values))
print("Expression 2 evaluates to:", expr2.subs(truth_values))
print("Expression 3 evaluates to:", expr3.subs(truth_values))
"""
# Convert the expressions to CNF and DNF forms
cnf_form = sympy.to_cnf(zi_expr)
dnf_form = sympy.to_dnf(expr3)

"""
print("CNF form of expression 2:", cnf_form)
print("DNF form of expression 3:", dnf_form)
"""
#print("Expression 1 evaluates to:", cnf_form.subs(truth_values))

KB = [expr1,expr2,expr3]
print(f"original {KB=}")

# Checking sat
for expr in KB[:]:
    #symbols = sorted([str(x) for x in expr.atoms()])
    print(expr.atoms())
    for arg in expr.atoms():
        truth_table = {k:(True if k==arg else False) for k in expr.atoms()}
        #print(f"{expr=} {truth_table=}")
        if expr.subs(truth_table) == True:
            print(f"{expr} only need {arg} True ")
            try:
                KB.remove(expr)
            except ValueError:
                pass 

            KB.append(arg)
            break
            

#removes identical values 
KB = list(dict.fromkeys(KB))
print(f" final {KB=}")
#Pure symbol

#Unit clause heuristic
