import time
import gurobipy as gp
from gurobipy import GRB

def solve_ilp_gurobi(n):
    start = time.perf_counter()
    model = gp.Model("NQueens")
    model.setParam('OutputFlag', 0)

    # Biến nhị phân x[i, j] = 1 nếu đặt hậu tại (i, j)
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

    # Mỗi hàng đúng 1 quân hậu
    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1)

    # Mỗi cột đúng 1 quân hậu
    for j in range(n):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1)

    # Đường chéo chính (\): r - c = k với k từ -(n - 1) đến n - 1
    for k in range(-(n - 1), n):
        diag_main = [x[r, r - k] for r in range(n) if 0 <= r - k < n]
        if len(diag_main) > 1:
            model.addConstr(gp.quicksum(diag_main) <= 1)

    # Đường chéo phụ (/): r + c = k với k từ 0 đến 2 * n - 2
    for k in range(2 * n - 1):
        diag_anti = [x[r, k - r] for r in range(n) if 0 <= k - r < n]
        if len(diag_anti) > 1:
            model.addConstr(gp.quicksum(diag_anti) <= 1)

    model.optimize()
    runtime = time.perf_counter() - start
    return model.status == GRB.OPTIMAL, runtime

if __name__ == "__main__":
    n = 8
    optimal, runtime = solve_ilp_gurobi(n)
    print(f"Optimal: {optimal}, Runtime: {runtime:.6f} seconds")