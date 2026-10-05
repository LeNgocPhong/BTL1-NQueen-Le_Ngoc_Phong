import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose3, Cadical153

def solve_sat(n, solver_name="glucose3"):
    start = time.perf_counter()
    vars_grid = [[i * n + j + 1 for j in range(n)] for i in range(n)]
    top_id = n * n
    clauses = []

    # Hàng & Cột: Exactly-One
    for i in range(n):
        cnf = CardEnc.equals(vars_grid[i], bound=1, top_id=top_id, encoding=EncType.pairwise)
        clauses.extend(cnf.clauses)
        top_id = cnf.nv
        
        col = [vars_grid[r][i] for r in range(n)]
        cnf = CardEnc.equals(col, bound=1, top_id=top_id, encoding=EncType.pairwise)
        clauses.extend(cnf.clauses)
        top_id = cnf.nv

    # Đường chéo: At-Most-One
    for d in range(-(n - 1), n):
        d1 = [vars_grid[r][r - d] for r in range(n) if 0 <= r - d < n]
        d2 = [vars_grid[r][d - r] for r in range(n) if 0 <= d - r < n]
        if len(d1) > 1:
            cnf = CardEnc.atmost(d1, bound=1, top_id=top_id, encoding=EncType.pairwise)
            clauses.extend(cnf.clauses)
            top_id = cnf.nv
        if len(d2) > 1:
            cnf = CardEnc.atmost(d2, bound=1, top_id=top_id, encoding=EncType.pairwise)
            clauses.extend(cnf.clauses)
            top_id = cnf.nv

    SolverClass = Glucose3 if solver_name == "glucose3" else Cadical153
    with SolverClass() as solver:
        solver.append_formula(clauses)
        sat = solver.solve()
    runtime = time.perf_counter() - start
    return sat, runtime

if __name__ == "__main__":
    n = 8
    sat, runtime = solve_sat(n)
    print(f"SAT: {sat}, Runtime: {runtime:.6f} seconds")