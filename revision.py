import sympy
import entrenchment
from DPLL import DPLL

def partial_m_contraction(belief_set,exp):
    remainders = []
    for belief in belief_set:
        if sympy.simplify(sympy.Implies(belief,exp)) == False:
            remainders.append(belief)
    return remainders        

def revision(belief_set,new_belief, symbols):
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

