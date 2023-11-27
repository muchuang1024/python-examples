from pulp import LpProblem, LpMaximize, LpVariable

# 创建线性规划问题
problem = LpProblem("My_LP_Problem", LpMaximize)

# 创建决策变量
x = LpVariable("x", lowBound=0)
y = LpVariable("y", lowBound=0)

# 添加目标函数
problem += 2 * x + 3 * y

# 添加约束条件
problem += x + 2 * y <= 6
problem += 2 * x + y <= 8

# 求解问题
problem.solve()

# 打印结果
print("x =", x.varValue)
print("y =", y.varValue)
