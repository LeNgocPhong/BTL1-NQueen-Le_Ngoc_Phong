import math
import time
from pysat.solvers import Glucose3

def solve_nqueens_binary_encoding(n):
    # Số bit cần thiết để biểu diễn chỉ số cột từ 0 đến n - 1
    k = math.ceil(math.log2(n)) if n > 1 else 1

    # Ánh xạ bit thứ b của hàng r sang biến SAT (1-based index)
    # r chạy từ 0 đến n - 1, b chạy từ 0 đến k - 1
    def bit_var(r, b):
        return r * k + b + 1

    clauses = []

    # 1. Cấm các giá trị cột không hợp lệ: c >= n (nếu 2^k > n)
    # Nếu một cấu hình bit tạo ra giá trị c >= n, phủ định cấu hình bit đó
    for r in range(n):
        for val in range(n, 1 << k):
            clause = []
            for b in range(k):
                if (val >> b) & 1:
                    clause.append(-bit_var(r, b))
                else:
                    clause.append(bit_var(r, b))
            clauses.append(clause)

    # Hàm tạo mệnh đề cấm: (hàng r1 chọn cột c1) VÀ (hàng r2 chọn cột c2)
    # ~(r1 == c1 AND r2 == c2) <=> ~(r1 == c1) OR ~(r2 == c2)
    def add_conflict(r1, c1, r2, c2):
        clause = []
        for b in range(k):
            # Nếu bit b của c1 là 1, phủ định là -bit_var, ngược lại là bit_var
            clause.append(-bit_var(r1, b) if ((c1 >> b) & 1) else bit_var(r1, b))
        for b in range(k):
            clause.append(-bit_var(r2, b) if ((c2 >> b) & 1) else bit_var(r2, b))
        clauses.append(clause)

    # 2. Xung đột giữa 2 hàng r1 và r2 (r1 < r2)
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            for c1 in range(n):
                for c2 in range(n):
                    # Cùng cột: c1 == c2
                    # Cùng đường chéo: |r1 - r2| == |c1 - c2|
                    if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                        add_conflict(r1, c1, r2, c2)

    # Khởi tạo solver Glucose3 và nạp tập mệnh đề
    solver = Glucose3()
    solver.append_formula(clauses)

    t0 = time.perf_counter()
    is_sat = solver.solve()
    runtime = time.perf_counter() - t0

    solution = None
    if is_sat:
        model = set(solver.get_model())
        solution = []
        for r in range(n):
            # Giải mã các bit để khôi phục chỉ số cột cho hàng r
            col = 0
            for b in range(k):
                if bit_var(r, b) in model:
                    col |= (1 << b)
            solution.append(col)

    solver.delete()
    return is_sat, runtime, solution, len(clauses), n * k

if __name__ == "__main__":
    n = 8
    is_sat, runtime, solution, num_clauses, num_vars = solve_nqueens_binary_encoding(n)
    
    print(f"N = {n}")
    print(f"Số biến: {num_vars}, Số mệnh đề: {num_clauses}")
    print(f"Satisfiable: {is_sat}")
    print(f"Thời gian solver: {runtime:.6f} giây")
    if is_sat:
        print(f"Vị trí các cột qua từng hàng: {solution}")