from ortools.sat.python import cp_model

# 1. Định nghĩa kích thước bàn cờ
N = 8

# 2. Khởi tạo đối tượng CP Model
model = cp_model.CpModel()

# 3. Tạo danh sách các biến quyết định:
# queens[i] đại diện cho chỉ số cột của quân hậu ở hàng i
queens = [model.NewIntVar(0, N - 1, f"queen_{i}") for i in range(N)]