import csv
import matplotlib.pyplot as plt

from sat_model import solve_n_queens
from cp_model import solve_cp_sat
from ilp_model import solve_ilp_gurobi

def benchmark_models(test_cases, output_csv="BTL1-NQueen-Le_Ngoc_Phong\\results\\benchmark_comparison.csv", chart_file="BTL1-NQueen-Le_Ngoc_Phong\\results\\benchmark_chart.png"):
    # Danh sách các solver cần so sánh: (Tên hiển thị, Hàm thực thi)
    solvers = [
        ("SAT (PySAT)", solve_n_queens),
        ("CP-SAT (OR-Tools)", solve_cp_sat),
        ("ILP (Gurobi)", solve_ilp_gurobi)
    ]
    
    results = []
    
    # In tiêu đề bảng
    header = f"{'N':<5} | " + " | ".join([f"{name:<18}" for name, _ in solvers])
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    
    for n in test_cases:
        row_data = {"N": n}
        row_str = f"{n:<5} | "
        
        for name, solver_func in solvers:
            try:
                # Gọi hàm giải và lấy runtime
                res = solver_func(n)
                runtime = res[1] if res and len(res) > 1 else None
                
                if runtime is not None:
                    row_data[name] = round(runtime, 6)
                    row_str += f"{runtime:<18.6f} | "
                else:
                    row_data[name] = "None"
                    row_str += f"{'None':<18} | "
            except Exception as e:
                # Bắt lỗi nếu solver gặp sự cố (ví dụ hết bộ nhớ hoặc lỗi timeout)
                row_data[name] = "Error"
                row_str += f"{'Error':<18} | "
                
        results.append(row_data)
        print(row_str)
        
    print("=" * len(header))
    
    # 1. Lưu kết quả ra file CSV
    fieldnames = ["N"] + [name for name, _ in solvers]
    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n[OK] Đã lưu bảng kết quả vào: {output_csv}")
    
    # 2. Vẽ biểu đồ đường so sánh thời gian chạy
    plot_comparison(results, solvers, chart_file)


def plot_comparison(results, solvers, chart_file):
    plt.figure(figsize=(10, 6))
    
    # Lấy trục hoành N
    n_values = [r["N"] for r in results]
    markers = ["o", "s", "^"]
    
    for idx, (name, _) in enumerate(solvers):
        times = []
        for r in results:
            val = r.get(name)
            # Chỉ vẽ các điểm có giá trị số hợp lệ
            if isinstance(val, (int, float)):
                times.append(val)
            else:
                times.append(None)
                
        plt.plot(n_values, times, marker=markers[idx % len(markers)], label=name, linewidth=2)

    plt.xlabel("Kích thước bàn cờ (N)", fontsize=12)
    plt.ylabel("Thời gian chạy (giây)", fontsize=12)
    plt.title("So sánh thời gian chạy giải bài toán N-Queens", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(chart_file, dpi=300)
    print(f"[OK] Đã lưu biểu đồ so sánh vào: {chart_file}")


if __name__ == "__main__":
    test_cases = [2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]
    
    benchmark_models(test_cases)