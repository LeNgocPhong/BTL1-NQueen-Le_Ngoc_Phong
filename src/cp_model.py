import time
from ortools.sat.python import cp_model

def solve_cp_sat(n):
    start = time.perf_counter()
    model = cp_model.CpModel()

    # queens[i] là chỉ số cột của quân hậu ở hàng i: domain [0, n - 1]
    queens = [model.NewIntVar(0, n - 1, f'q_{i}') for i in range(n)]

    # 1. Ràng buộc các cột khác nhau
    model.AddAllDifferent(queens)

    # 2. Ràng buộc đường chéo chính và chéo phụ
    # queens[i] - i và queens[i] + i phải đôi một khác nhau
    model.AddAllDifferent([queens[i] + i for i in range(n)])
    model.AddAllDifferent([queens[i] - i for i in range(n)])

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1  # Đặt 1 thread để so sánh công bằng
    status = solver.Solve(model)
    runtime = time.perf_counter() - start

    return status in (cp_model.OPTIMAL, cp_model.FEASIBLE), runtime

if __name__ == "__main__":
    n = 8
    feasible, runtime = solve_cp_sat(n)
    print(f"Feasible: {feasible}, Runtime: {runtime:.6f} seconds")