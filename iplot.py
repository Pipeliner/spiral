import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])
plt.ion()

y_old = 0.5

for i in range(10):
    y = np.random.random()
    plt.plot([i, i+1], [y_old, y])
    y_old = y
    plt.pause(0.5)

