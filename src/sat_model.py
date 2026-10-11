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
            clause = get_blocking_clause_for_value(board_vars[i], val, K)
            cnf.append(clause)

def get_blocking_pair_clause(row_i_vars, val_i, row_j_vars, val_j, K):
    clause = []
    for k in range(K):
        bit_i = (val_i >> (K-1-k)) & 1
        clause.append(-row_i_vars[k] if bit_i == 1 else row_i_vars[k])
    for k in range(K):
        bit_j = (val_j >> (K - 1 - k)) & 1
        clause.append(-row_j_vars[k] if bit_j  == 1 else row_j_vars[k])
    return clause

def add_column_constraints(cnf, board_vars, N, K):
    for i in range(N):
        for j in range(i + 1, N):
            for c in range(N):
                clause = get_blocking_pair_clause(board_vars[i], c, board_vars[j], c, K)
                cnf.append(clause)

def add_diagonal_constraints(cnf, board_vars, N, K):
    for i in range(N):
        for j in range(i + 1, N):
            delta = j-i
            for c_i in range(N):
                c_j_right = c_i + delta
                if c_j_right < N:
                    clause = get_blocking_pair_clause(board_vars[i], c_i, board_vars[j], c_j_right, K)
                    cnf.append(clause)
                c_j_left = c_i - delta
                if c_j_left >= 0:
                    clause = get_blocking_pair_clause(board_vars[i], c_i, board_vars[j], c_j_left, K)
                    cnf.append(clause)

def solve_n_queens(cnf):
    with Glucose3(bootstrap_with=cnf) as solver:
        if solver.solve():
            return solver.get_model()
    return None

def decode_model_to_positions(model, board_vars, N, K):
    if model is None:
        return None
    model_set = set(model)
    queens_positions = []
    for r in range(N):
        col = 0
        for k in range(K):
            if board_vars[r][k] in model_set:
                col |= (1 << (K - 1 - k))
    queens_positions.append(col)
    return queens_positions

def display_board(queens_positions, N):
    if queens_positions is None:
        print(f"Bai toan {N}-Queens vo nghiem (UNSAT).")
        return
    
    print(f"=== KẾT QUẢ BÀI TOÁN {N}-QUEENS ===")
    print(f"Tọa độ cột từng hàng: {queens_positions}\n")
    
    for r in range(N):
        row_str = " ".join("Q" if c == queens_positions[r] else "." for c in range(N))
        print(f"Hàng {r}: {row_str}")
    print()
