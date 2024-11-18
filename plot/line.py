import matplotlib.pyplot as plt

import numpy as np


x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)


fig, ax = plt.subplots()


ax.plot(x, y)


ax.set_xticks(np.arange(10))

ax.set_xticklabels(["一", "三", "三", "四", "五", "六", "七", "八", "九", "十"])

ax.set_yticks(np.arange(-1, 1.5, 0.5))

ax.set_yticklabels(["低", "中低", "中", "中高", "高"])


plt.show()
