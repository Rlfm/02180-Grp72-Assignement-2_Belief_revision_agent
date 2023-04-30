from sympy import FiniteSet, Intersection, to_cnf, to_dnf
import entrenchment
from DPLL import DPLL

def find_minimal_state(knowledgeBase):
    #propositions = []
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
    propositions = current_minimal_state.keys()
    symbols = new_belief.free_symbols
    s = DPLL([new_belief],symbols)
    rs = s[1].keys()
    list_other_s = propositions
    #for i in rs:
    #    list_other_s.remove(i)
    #other_s = {i: True for i in list_other_s}
    other_s = current_minimal_state
    state = other_s | s[1]
    beliefBase_state = knowledgeBase.subs(state)
    KB = []
    for k in range(0,len(knowledgeBase.args)):
        if knowledgeBase.args[k].subs(state) == True:
            KB.append(knowledgeBase.args[k])
    KB = FiniteSet(*KB)
    new_knowledgeBase = Intersection(knowledgeBase,KB)
    AGM_Rationality_Postulates_for_contraction(knowledgeBase, new_belief, new_knowledgeBase, current_minimal_state)
    return new_knowledgeBase, state

def adding_new(knowledgeBase, new_belief):
    KB = []
    for i in knowledgeBase:
        KB.append(i)
    KB.append(new_belief)
    new_knowledgeBase = FiniteSet(*KB)
    AGM_Rationality_Postulates_for_expansion(knowledgeBase, new_belief, new_knowledgeBase)
    return new_knowledgeBase

def revision(knowledgeBase, new_belief, current_minimal_state):
    knowledgeBase, minimal_state_after_revision = contraction_using_plausibility_order(knowledgeBase, new_belief, current_minimal_state)
    knowledgeBase = adding_new(knowledgeBase,new_belief)
    return knowledgeBase, minimal_state_after_revision

def AGM_Rationality_Postulates_for_contraction(KB, expr, KB_post_contraction, current_minimal_state):
    """
    functions that assess that AGM postulates are respected for the present contraction 
    """
    expr = to_cnf(expr)
    # Success
    assert expr not in KB_post_contraction, f"{expr} is still part of KB after contraction"

    # Inclusion 
    assert len([x for x in KB_post_contraction if x in KB]) == len(KB_post_contraction), "KB after contraction is not a subset of original KB"

    # Vacuity 
    if expr not in KB:
        assert KB == KB_post_contraction, f"KB was modified but {expr} wasn't in KB"

    # Extensionality
    expr2 = to_dnf(expr)
    X,Y = contraction_using_plausibility_order(KB, expr2, current_minimal_state)
    assert KB_post_contraction == X, "The outcomes of contracting with equivalent sentences are not equal"

def AGM_Rationality_Postulates_for_expansion(KB, expr, KB_post_expansion):
    """
    functions that asses that AGM postulates are respected for the present expansion. 
    """
    # Sucess 
    assert {expr} not in KB_post_expansion, f"{expr} is still part of KB after expansion"

    # Inclusion
    assert all(x in KB.copy().append(expr) for x in KB_post_expansion), "KB after revision is not a subset of original KB after expansion"

    # Vacuity
    if expr not in KB:
        assert KB == KB_post_expansion, "KB was modified but {expr} wasn't in KB"

    # Consistency
    if consistensy(expr):
        assert consistensy(KB_post_expansion), f"{expr} is consisten but, KB after expansion is not"
    
    # Extensionality
    expr2 = to_dnf(expr)
    assert KB_post_expansion == adding_new(KB, expr2), "The outcomes of contracting with equivalent sentences are not equal"

def consistensy(Set):
    """
    Returns if a set of beliefs is consistent.
    """
    result, list = DPLL(Set)
    return result