import sympy

# Define some symbols
A, B, C = sympy.symbols('A B C')

# Define some logical expressions
expr1 = sympy.And(A, B)
expr2 = sympy.Or(expr1, C)
expr3 = sympy.Implies(A, B)

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

print("Expression 1 evaluates to:", expr1.subs(truth_values))
print("Expression 2 evaluates to:", expr2.subs(truth_values))
print("Expression 3 evaluates to:", expr3.subs(truth_values))

# Convert the expressions to CNF and DNF forms
cnf_form = sympy.to_cnf(expr2)
dnf_form = sympy.to_dnf(expr3)

print("CNF form of expression 2:", cnf_form)
print("DNF form of expression 3:", dnf_form)
