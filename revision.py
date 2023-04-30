import sympy
from sympy import FiniteSet, Intersection, to_cnf, to_dnf
import entrenchment
from DPLL import DPLL

def find_minimal_state(knowledgeBase):

    # This function finds the minimal state of a knowledgeBase
    
    symbols_true = knowledgeBase.free_symbols
    symbols_false = set()
    for formula in knowledgeBase:
        if len(formula.args) == 1 and formula != formula.free_symbols:
            symbols_true.remove(formula.args[0])
            symbols_false = symbols_false | formula.free_symbols
    minimal_state = {i: True for i in symbols_true}
    add_state = {i: False for i in symbols_false}
    minimal_state = minimal_state | add_state
    return minimal_state

def contraction_using_plausibility_order(knowledgeBase, new_belief, current_minimal_state):

    # This function takes new_belief as an argument but contracts the knowledgeBase by not(new_belief)

    propositions = current_minimal_state.keys()
    symbols = new_belief.free_symbols
    s = DPLL([new_belief],symbols)
    other_s = current_minimal_state
    state = other_s | s[1]
    KB = []
    for k in range(0,len(knowledgeBase.args)):
        if knowledgeBase.args[k].subs(state) == True:
            KB.append(knowledgeBase.args[k])
    KB = FiniteSet(*KB)
    new_knowledgeBase = Intersection(knowledgeBase,KB)
    return new_knowledgeBase, state

def adding_new(knowledgeBase, new_belief):

    # This function simply add a new_belief to the knowledgeBase 

    KB = []
    for i in knowledgeBase:
        KB.append(i)
    KB.append(new_belief)
    new_knowledgeBase = FiniteSet(*KB)
    return new_knowledgeBase

def revision(knowledgeBase, new_belief, current_minimal_state, check_revision_with_AGM=False):

    # This function returns new knowledge base (revising the knowledge base by a new belief) and new minimal state 

    original_knowledgeBase = knowledgeBase
    new_knowledgeBase, minimal_state_after_revision = contraction_using_plausibility_order(knowledgeBase, new_belief, current_minimal_state)
    AGM_Rationality_Postulates_for_contraction(knowledgeBase, new_belief, new_knowledgeBase, current_minimal_state)
    knowledgeBase = new_knowledgeBase
    new_knowledgeBase = adding_new(knowledgeBase,new_belief)
    if check_revision_with_AGM == True:
        AGM_Rationality_Postulates_for_expansion(original_knowledgeBase, new_belief, new_knowledgeBase, current_minimal_state)
    return knowledgeBase, minimal_state_after_revision

def AGM_Rationality_Postulates_for_contraction(knowledgeBase, new_belief, new_knowledgeBase, current_minimal_state):

    # Functions that assess that AGM postulates are respected for the present contraction 

    KB = []
    for i in knowledgeBase:
        KB.append(i)
    expr = sympy.simplify(sympy.Not(new_belief))                 # If knowledge base is to be revised by new belief, the contraction is done by not(new_belief)
    KB_post_contraction = []
    for i in new_knowledgeBase:
        KB_post_contraction.append(i)

    # Success
    assert expr not in KB_post_contraction, f"{expr} is still part of KB after contraction"

    # Inclusion 
    assert len([x for x in KB_post_contraction if x in KB]) == len(KB_post_contraction), "KB after contraction is not a subset of original KB"

    a = expr.free_symbols
    b =  knowledgeBase.free_symbols
    # Vacuity 
    if not(expr.free_symbols.issubset(knowledgeBase.free_symbols)):
        assert KB == KB_post_contraction, f"KB was modified but {expr} wasn't in KB"

    # Extensionality
    expr2 = to_dnf(new_belief)
    X,Y = contraction_using_plausibility_order(knowledgeBase, expr2, current_minimal_state)
    assert new_knowledgeBase == X, "The outcomes of contracting with equivalent sentences are not equal"

def AGM_Rationality_Postulates_for_expansion(knowledgeBase, expr, new_knowledgeBase, current_minimal_state):

    # functions that asses that AGM postulates are respected for the present expansion. 

    KB = []
    for i in knowledgeBase:
        KB.append(i)
    KB_post_revision = []
    for i in new_knowledgeBase:
        KB_post_revision.append(i)
    print(new_knowledgeBase)
    # Sucess 
    assert {expr} not in KB_post_revision, f"{expr} is still part of KB after expansion"

    # Inclusion
    assert set(KB_post_revision).issubset(set(adding_new(knowledgeBase,expr))), "KB after revision is not a subset of original KB after expansion"

    # Vacuity
    if not(expr.free_symbols.issubset(knowledgeBase.free_symbols)):
        assert KB == KB_post_revision, "KB was modified but {expr} wasn't in KB"

    # Consistency
    if consistency({expr}, [x for x in expr.free_symbols]):
        assert consistency(KB_post_revision, [x for x in new_knowledgeBase.free_symbols]), f"{expr} is consisten but, KB after expansion is not"
    
    # Extensionality
    expr2 = to_dnf(expr)
    revised, minimal_state = revision(knowledgeBase, expr2, current_minimal_state, False)
    assert new_knowledgeBase == revised, "The outcomes of contracting with equivalent sentences are not equal"

def consistency(Set, symbols):

    # Returns True if a set of beliefs is consistent.

    result, list = DPLL(Set, symbols)
    return result