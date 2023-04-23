import sympy


def isMoreEntrenched_1(p,q):
    """Determines if p is more entrenched than q by checking only implication"""

    if sympy.simplify(sympy.Implies(p,q)) == True:
        return False
    
    else: return True

def isMoreEntrenched_2(p,q):
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
    



# Testing code
if __name__ == "__main__":
    A, B, C, D, E, F = sympy.symbols('A B C D E F')
    p = sympy.Implies(E,D)
    q = sympy.Equivalent(A,(C | E))
    
    print(isMoreEntrenched_1(p,q))
    print(isMoreEntrenched_1(q,p))

    print(isMoreEntrenched_2(p,q))
    print(isMoreEntrenched_2(q,p))