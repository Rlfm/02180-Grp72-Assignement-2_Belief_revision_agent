import sympy
from sympy import FiniteSet, Intersection, Union
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
    knowledgeBase = Intersection(knowledgeBase,KB)
    return knowledgeBase, state

def adding_new(knowledgeBase, new_belief):
    KB = []
    for i in knowledgeBase:
        KB.append(i)
    KB.append(new_belief)
    knowledgeBase = FiniteSet(*KB)
    return knowledgeBase

def revision(knowledgeBase, new_belief, current_minimal_state):
    #not_new_belief = sympy.simplify(sympy.Not(new_belief))
    knowledgeBase, minimal_state_after_revision = contraction_using_plausibility_order(knowledgeBase,new_belief, current_minimal_state)
    knowledgeBase = adding_new(knowledgeBase,new_belief)
    return knowledgeBase, minimal_state_after_revision

def partial_m_contraction(belief_set,exp):
    remainders = []
    for belief in belief_set:
        if sympy.simplify(sympy.Implies(belief,exp)) == False:
            remainders.append(belief)
    return remainders        

def old_revision(belief_set,new_belief, symbols):
    not_subset = []
    inconsistency = []
    for belief in belief_set:
        two_exp = [belief,new_belief]
        k = DPLL(two_exp,symbols)
        if k[0] == False:
            not_subset.append(belief)
        else:
            inconsistency.append(belief)
    if len(inconsistency)==0:
        belief_set.append(new_belief)
        new_belief_set = belief_set
        return new_belief_set
    else:
        for a in inconsistency:
            for i in range(0,len(a.args)):
                two_exp = [a.args[i],new_belief]
                k = DPLL(two_exp,symbols)
                if k[0]==False:
                    if a.args[i].atoms()==1:
                        a.args[i] = new_belief
        sorted_subset = entrenchment.reorder_expressions(inconsistency)
        sorted_subset.reverse()
        for test in sorted_subset:
            test_set = sorted_subset
            test_set.remove(test)
            new_belief_set = test_set
            new_belief_set.extend(not_subset) 
            k = DPLL(new_belief_set,symbols)

