# 02180-Grp72-Assignement-2

**Method I: Belief Revision based on partial meet contraction and entrenchment**
  
**How to run the script**

Make sure *sympy* is correctly installed.

Then, simply run the following command in the installation folder containing all the python files:

python BeliefBase.py

**Included Python files**

The included Python files are the following:

- DPLL.py: implements the DPLL algorithm for checking logical entailment
- entrenchment.py: implements functions for reordering expressions based on entrenchment
- contraction.py: implements functions for contracting belief bases and for assessing AGM postulates for a given contraction
- revision.py: implements functions for expanding belief bases and for assessing AGM postulates for a given expansion 
- BeliefBase.py: Allows the testing of the implemented functions on a given belief base.

**Method II - Revision based on Plausibility Order**

**How to run the script**

Prerequisite: *sympy* is correctly installed.

To test the code with different belief statements. Edit the *Belief statement* and *new_belief* in the *main.py*
Then, run the following command in the installation folder containing all the python files:

python main.py

**Included Python files**

The included Python files are the following:

- main.py: Allows the testing of the implemented functions on a given belief base.
- DPLL.py: implements the DPLL algorithm for checking logical entailment
- revision.py: implements contraction and revision of belief bases and assess AGM postulates for both.