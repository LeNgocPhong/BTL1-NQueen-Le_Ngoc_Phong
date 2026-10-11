import time
import math
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose3, Cadical153

def init_board_variables(N):
    K = math.ceil(math.log2(N))
    board_vars = []
    var_id = 1
    
    for row in range(N):
        row_bits = []
        for bit in range(K):
            row_bits.append(var_id)
            var_id += 1
        board_vars.append(row_bits)
        
    return board_vars, K

def get_blocking_clause_for_value(row_vars, val, K):
    clause = []
    for k in range(K):
        bit = (val >> (K - 1 - k)) & 1
        var = row_vars[k]

        if bit == 1:
            clause.append(-var)
        else:
            clause.append(var)
    return clause

def add_domain_constraints(cnf, board_vars, N, K):
    max_val = 1 << K
    for i in range(N):
        for val in range(N, max_val):
            clause = get_bloking_clause_for_value(board_vars[i], val, K)
            cnf.append(clause)
