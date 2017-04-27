#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

center = 7
side = center*2
def distFromOrigin(x, y, old_dx, dx, old_dy, dy):
    ax, ay = x - center, y - center
    bx, by = old_dx - center, old_dy - center
    angle_tan = np.float64(1.0) * (ax * by - ay * bx) / (ax * bx + ay * by)
    return ((center - x)**2 + (center - y)**2, angle_tan, -(old_dx*dx + old_dy*dy))
    #return (-(old_dx*dx + old_dy*dy), (center - x)**2 + (center - y)**2)

import numpy as np
x, y = center, center
x_old, y_old = center + 1, center + 1
marked = np.full((side,side), False, dtype=bool)
marked[y][x] = True
xs = [x]
ys = [y]

while x > 1 and x < side - 2 and y > 1 and y < side - 2:
    best_dx = 1
    best_dy = 1
    best_dist = (100000,-1000)
    old_dx, old_dy = x - x_old, y - y_old
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x_new = x + dx
            y_new = y + dy
            if (dx != 0 or dy != 0) and (dx, dy) != (old_dx, old_dy) and not marked[y_new][x_new]:
                dist = distFromOrigin(x_new, y_new, old_dx, dx, old_dy, dy)
                print dist
                if dist < best_dist:
                    best_dist = dist
                    best_dx = dx
                    best_dy = dy
    
    #print (best_dx, best_dy, best_dist)
    x_new = x + best_dx
    y_new = y + best_dy
    xs.append(x_new)
    ys.append(y_new)
    marked[y_new][x_new] = True
    x_old, y_old, x, y = x, y, x_new, y_new

plt.plot(xs, ys)
plt.show()
