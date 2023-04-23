import sympy


def is_more_entrenched_1(p,q):
    """Determines if p is more entrenched than q by checking only implication"""

    if sympy.simplify(sympy.Implies(p,q)) == True:
        return False
    
    else: return True

def is_more_entrenched_2(p,q):
    """Determines if p is more entrenched than q by checking implication and number of atoms"""

    p_implies_q = sympy.Implies(p, q)
    q_implies_p = sympy.Implies(q, p)

    if sympy.simplify(p_implies_q) == True and sympy.simplify(q_implies_p) != True:
        return False
    elif sympy.simplify(q_implies_p) == True and sympy.simplify(p_implies_q) != True:
        return True
    else:
        # Returns True if p has fewer operators than q
        p_ops = len(list(p.atoms()))
        q_ops = len(list(q.atoms()))
        return p_ops < q_ops
    


def reorder_expressions(expressions):
    """
    Returns a new list of expressions reordered based on their entrenchment,
    from most entrenched to least entrenched.
    input is a list of Sympy expressions.
    """

    # Compute entrenchment for each expression
    entrenchments = []
    for i, e in enumerate(expressions):
        entrenchment = 0
        for j, f in enumerate(expressions):
            if i != j:
                if is_more_entrenched_2(f, e):
                    entrenchment += 1
                elif is_more_entrenched_2(e, f):
                    entrenchment -= 1
        entrenchments.append(entrenchment)
    
    # Sort expressions by entrenchment
    sorted_indices = sorted(range(len(expressions)), key=lambda i: -entrenchments[i])
    return [expressions[i] for i in sorted_indices]


# Testing code
if __name__ == "__main__":

    A, B, C, D, E, F = sympy.symbols('A B C D E F')

    p = sympy.Equivalent(A,(C | E))
    q = sympy.Implies(E,D)
    r = sympy.Implies((B & F),sympy.Not(C))
    t = sympy.Implies(E,C)
    v = C >> F 
    u = C >> B 

    exprs = [p,q,r,t,v,u]
    
    print(is_more_entrenched_1(p,q))
    print(is_more_entrenched_1(q,p))

    print(is_more_entrenched_2(p,q))
    print(is_more_entrenched_2(q,p))

    print(reorder_expressions(exprs))