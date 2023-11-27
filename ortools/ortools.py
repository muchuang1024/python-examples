from ortools.linear_solver import pywraplp

# 创建线性规划求解器
solver = pywraplp.Solver.CreateSolver("SCIP")

# 添加变量
x = solver.IntVar(0.0, 1.0, "x")
y = solver.IntVar(0.0, 2.0, "y")

# 设置目标函数
solver.Minimize(x + 2 * y)

# 添加约束条件
solver.Add(x + 2 * y >= 2)
solver.Add(x + y <= 3)

# 求解问题
solver.Solve()

# 打印结果
