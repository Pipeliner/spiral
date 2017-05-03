#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

center = 25
side = center*2
def distFromOrigin(x, y, old_dx, dx, old_dy, dy):
    ax, ay = x - center, y - center
    bx, by = old_dx - center, old_dy - center
    angle_tan = np.float64(1.0) * (ax * by - ay * bx) / (ax * bx + ay * by)
    if angle_tan < 0:
        angle_tan = 20

    distance_from_center = (center - x)**2 + (center - y)**2
    scalar_product_with_previous = old_dx*dx + old_dy*dy

    a = 1
    b = 0
    c = 0
    return a * distance_from_center - b * scalar_product_with_previous - c * angle_tan
    #return angle_tan
    #return (-(old_dx*dx + old_dy*dy), (center - x)**2 + (center - y)**2)

import numpy as np
x, y = center, center
x_old, y_old = center + 1, center + 1
marked = np.full((side,side), False, dtype=bool)
marked[y][x] = True
xs = [x]
ys = [y]

plt.axis([0, side, 0, side])
plt.ion()

while x > 1 and x < side - 2 and y > 1 and y < side - 2:
    print ("Considering next point from (%s, %s)" % (x, y))
    best_dx = 1
    best_dy = 1
    best_dist = 100000
    old_dx, old_dy = x - x_old, y - y_old
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x_new = x + dx
            y_new = y + dy
            if (dx != 0 or dy != 0) and (dx, dy) != (old_dx, old_dy) and not marked[y_new][x_new]:
                dist = distFromOrigin(x_new, y_new, old_dx, dx, old_dy, dy)
                print ("(%s, %s)" % (x_new, y_new), dist)
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

    #plt.plot([x, x_new], [y, y_new])
    plt.plot([x_old, x], [y_old, y])
    #print([x, x_new], [y, y_new])
    #raw_input()
    plt.pause(0.01)
    

#plt.plot(xs, ys)
plt.show()
raw_input()
