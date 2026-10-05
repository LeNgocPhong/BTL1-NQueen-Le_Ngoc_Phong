import time
import gurobipy as gp
from gurobipy import GRB

def solve_ilp_gurobi(n):
    start = time.perf_counter()
    model = gp.Model("NQueens")
    model.setParam('OutputFlag', 0)  # Tắt log in ra console

    # Biến nhị phân x[i, j] = 1 nếu đặt hậu tại (i, j)
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

    # Mỗi hàng đúng 1 quân hậu
    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1)

    # Mỗi cột đúng 1 quân hậu
    for j in range(n):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1)

    # Đường chéo tối đa 1 quân hậu
    for d in range(-(n - 1), n):
        d1 = [x[r, r - d] for r in range(n) if 0 <= r - d < n]
        d2 = [x[r, d - r] for r in range(n) if 0 <= d - r < n]
        if len(d1) > 1:
            model.addConstr(gp.quicksum(d1) <= 1)
        if len(d2) > 1:
            model.addConstr(gp.quicksum(d2) <= 1)

    model.optimize()
    runtime = time.perf_counter() - start
    return model.status == GRB.OPTIMAL, runtime

if __name__ == "__main__":
    n = 8
    optimal, runtime = solve_ilp_gurobi(n)
    print(f"Optimal: {optimal}, Runtime: {runtime:.6f} seconds")