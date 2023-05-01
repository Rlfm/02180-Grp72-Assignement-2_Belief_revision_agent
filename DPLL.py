import logging 

level = logging.INFO	
fmt = '[%(levelname)s] {%(filename)s, %(funcName)s} %(asctime)s - %(message)s'
logging.basicConfig(level =level, format=fmt)

def FIND_PURE(cnf_KB,symbols):
    for symb in symbols:
        truth_table = {symb:True}
        try:
            for expr in cnf_KB:
    
                if f"~{symb}" in str(expr):
                    raise ValueError(f"[{symb} is not pure -> {expr}]")

            return symb
        except ValueError as err:
            logging.debug(err)
    
    return False

def FIND_UNIT(cnf_KB,symbols):
    for expr in cnf_KB:
        if len(expr.atoms()) == 1:
            
            logging.debug(f"UNIT CLAUSE found: {expr}")

            if "~" in str(expr):
                return list(expr.atoms())[0], False
            else:
                return list(expr.atoms())[0], True

    return False

def DPLL(cnf_KB,symbols,model={}):
    
    logging.debug(cnf_KB)
    if len(cnf_KB) == 0:
        return True,model

    if False in cnf_KB:
        return False, None
        
    UNIT_CLAUSE = FIND_UNIT(cnf_KB,symbols)
    PURE_SYMBOL = FIND_PURE(cnf_KB,symbols)


    if UNIT_CLAUSE != False:

        P = UNIT_CLAUSE[0] 
        logging.debug(f"UNIT_CLAUSE chosen chosing {P} = {UNIT_CLAUSE[1]}")

        if UNIT_CLAUSE[1]:
            model[P] = True
            new_KB = [expr.subs({P:True}) for expr in cnf_KB if expr.subs({P:True}) != True]
        else:
            model[P] = False 
            new_KB = [expr.subs({P:False}) for expr in cnf_KB if expr.subs({P:False}) != True]

        new_symbols = [x for x in symbols if x!= UNIT_CLAUSE]

        DPLL_sat_return = DPLL(new_KB, new_symbols,model)
        
        assert DPLL_sat_return, "Model not SAT, unit clause should always be SAT"
        return DPLL_sat_return
       
    elif PURE_SYMBOL != False:
        P = PURE_SYMBOL
        logging.debug(f"PURE SYMBOL chosing {P=}") 
        model[P] = True
        new_KB = [expr.subs({P:True}) for expr in cnf_KB if expr.subs({P:True}) != True]
        new_symbols = [x for x in symbols if x!= PURE_SYMBOL]

        DPLL_sat_return = DPLL(new_KB, new_symbols,model)

        assert DPLL_sat_return, "Model not SAT, pure symbol should always be SAT"
        return DPLL_sat_return  

    else:
        for symbol in symbols:
            P = symbol
            logging.debug(f"CLASSICAL chosing {P=} True")
            model[P] = True

            new_KB = [expr.subs({P:True}) for expr in cnf_KB if expr.subs({P:True}) != True]
            new_symbols = [x for x in symbols if x!= symbol]
            DPLL_sat_return = DPLL(new_KB, new_symbols)

            if DPLL_sat_return[0] == False:
                logging.debug(f"CLASSICAL chosing {P=} False")
                model[P] = False
                new_KB = [expr.subs({P:False}) for expr in cnf_KB if expr.subs({P:False}) != True]
                DPLL_sat_return = DPLL(new_KB, new_symbols,model)
            
            return DPLL_sat_return
