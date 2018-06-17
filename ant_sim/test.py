import numpy as np
import matplotlib.pyplot as plt
from ant_sim.atractors import PheromoneManager as PM



N = 1000
x, y = np.random.rand(N), np.random.rand(N)
v = zip(x, y)
X, Y, R = .5, .5, .3

valid = filter(lambda p: (X - R < p[0] < X + R) and (Y - R < p[1] < Y + R), v)
valid = filter(lambda p: PM.length([X - p[0], Y - p[1]]) < R, valid)
valid = filter(lambda p: PM.angle_between([X, Y], [p[0] - X, p[1] - Y]) < 10, valid)
v = zip(*valid)

plt.scatter(x, y, color='b')
plt.scatter(x=v[0], y=v[1], color='r')
plt.show()
