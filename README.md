# N-Queens Solver: SAT Binary Encoding & Benchmark

Dự án giải bài toán $N$-Queens tập trung vào mô hình hóa **SAT với Binary Encoding (PySAT/Glucose3)**, đồng thời đo lường và so sánh hiệu năng đối chuẩn với **CP-SAT (OR-Tools)** và **ILP (Gurobi)**.

---

### Cấu trúc thư mục

```text
BTL1-NQueen/
├── src/
│   ├── sat_model.py               # [Trọng tâm] Mã hóa CNF nhị phân & giải bằng PySAT (tự xây dựng)
│   ├── example_sat_model.py       # [Trọng tâm] Mã hóa CNF nhị phân & giải bằng PySAT (code mẫu)
│   ├── cp_model.py                # [Baseline] Mô hình CP-SAT (OR-Tools) (code mẫu)
│   ├── ilp_model.py               # [Baseline] Mô hình ILP (Gurobi) (code mẫu)
│   └── benchmark.py               # Tự động so sánh thời gian, xuất CSV & biểu đồ
├── results/
│   ├── benchmark_comparison.csv
│   └── benchmark_chart.png
└── README.md

```

---

### Cách vận hành

1. **Cài đặt thư viện:**

```bash
pip install python-sat ortools gurobipy matplotlib

```

2. **Chạy mô hình trọng tâm SAT:**

```bash
python src/sat_model.py

```

3. **Chạy benchmark so sánh toàn bộ mô hình:**

```bash
python src/benchmark.py

```

_(Kết quả in bảng thời gian ra terminal, lưu dữ liệu vào `results/benchmark_comparison.csv` và vẽ biểu đồ tại `results/benchmark_chart.png`)_
