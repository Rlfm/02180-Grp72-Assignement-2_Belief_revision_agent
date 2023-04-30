import sympy
from sympy import FiniteSet, Intersection, Union
import entrenchment
from DPLL import DPLL
import AGM_postulates

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
    AGM_postulates.AGM_Rationality_Postulates_for_contraction(knowledgeBase, new_belief, new_knowledgeBase, current_minimal_state)
    return new_knowledgeBase, state

def adding_new(knowledgeBase, new_belief):
    KB = []
    for i in knowledgeBase:
        KB.append(i)
    KB.append(new_belief)
    new_knowledgeBase = FiniteSet(*KB)
    AGM_postulates.AGM_Rationality_Postulates_for_expansion(knowledgeBase, new_belief, knowledgeBase)
    return new_knowledgeBase

def revision(knowledgeBase, new_belief, current_minimal_state):
    #not_new_belief = sympy.simplify(sympy.Not(new_belief))
    knowledgeBase, minimal_state_after_revision = contraction_using_plausibility_order(knowledgeBase, new_belief, current_minimal_state)
    knowledgeBase = adding_new(knowledgeBase,new_belief)
    return knowledgeBase, minimal_state_after_revision
