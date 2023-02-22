# Gift Wrapping Algorithm (Jarvis march) Implementation - old version
# - Author: Tomash Mikulevich
# - Created with: PyCharm 2022.2.1 (Professional Edition - Student Pack)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Tigers:
    def __init__(self, num):
        self.num = num
        self.tigers = []

    def getTigers(self):
        return self.tigers

    def generateTigers(self):
        xy = [[np.random.uniform(-50, 50), np.random.uniform(-50, 50)] for i in range(self.num)]
        self.tigers = xy


def jarvisAlg(i):
    if i < np.size(jTigersX1):
        Sp = [jTigersX1[i], jTigersY1[i]]
        Np = min(tigers, key=lambda point: angleAndDist(Sp, point))

        if np.array_equal(Np, [jTigersX2[0], jTigersY2[0]]):
            jTigersX1.append(Np[0])
            jTigersY1.append(Np[1])

        jTigersX1.append(Np[0])
        jTigersY1.append(Np[1])

    if i < np.size(jTigersX2):
        Sq = [jTigersX2[i], jTigersY2[i]]
        Nq = min(tigers, key=lambda point: angleAndDist(point, Sq))

        if np.array_equal(Nq, [jTigersX1[0], jTigersY1[0]]):
            jTigersX2.append(Nq[0])
            jTigersY2.append(Nq[1])

        jTigersX2.append(Nq[0])
        jTigersY2.append(Nq[1])

    jTigersLine1.set_data(jTigersX1, jTigersY1)
    jTigersLine2.set_data(jTigersX2, jTigersY2)

    # if np.array_equal(Np, [jTigersX2[0], jTigersY2[0]]) and np.array_equal(Nq, [gTigersX1[0], jTigersY1[0]]):
    #    break

    return jTigersLine1, jTigersLine2


def angleAndDist(point1, point2):
    dx, dy = point1[0] - point2[0], point1[1] - point2[1]

    return np.arctan2(dy, dx)


fig = plt.figure()
ax = plt.axes()

N = 40
zoo = Tigers(N)
zoo.generateTigers()
tigers = zoo.getTigers()

tigersX, tigersY = list(list(zip(*tigers))[0]), list(list(zip(*tigers))[1])
plt.plot(tigersX, tigersY, 'ro', markersize=5)

jTigersX1, jTigersY1 = [min(tigers, key=lambda point: point[1])[0]], [min(tigers, key=lambda point: point[1])[1]]
jTigersX2, jTigersY2 = [max(tigers, key=lambda point: point[1])[0]], [max(tigers, key=lambda point: point[1])[1]]
jTigersLine1, = ax.plot(jTigersX1, jTigersY1, '--bo', markersize=2, linewidth=1)
jTigersLine2, = ax.plot(jTigersX2, jTigersY2, '--bo', markersize=2, linewidth=1)

animate = FuncAnimation(fig, func=jarvisAlg, frames=np.size(tigersX), interval=500, repeat=False)

plt.show()
