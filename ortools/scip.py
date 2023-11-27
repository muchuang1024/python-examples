import numpy as np
from scipy.optimize import minimize


# 定义目标函数 f(x) = x^2 - 4x + 4
def objective(x):
    return x[0] ** 2 - 4 * x[0] + 4


# 定义约束条件（无约束）
constraints = ()

# 定义初始点
initial_x = np.array([0.0])

# 使用内点法进行优化
result = minimize(objective, initial_x, constraints=constraints, method="trust-constr")

if result.success:
    # 输出最优解和最小值
    print("最优解: x =", result.x)
    print("最小值: f(x) =", result.fun)
else:
    print("优化过程出错:", result.message)
