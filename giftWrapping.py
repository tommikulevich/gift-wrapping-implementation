# Gift Wrapping Algorithm (Jarvis march) Implementation
# - Author: Tomash Mikulevich
# - Created with: PyCharm 2022.2.1 (Professional Edition - Student Pack)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from matplotlib.path import Path


class Tigers:
    def __init__(self, num):
        self._num = num
        self._tigXY = []
        self._tigVert3XY = []
        self._tigVertAllXY = []
        self._tigAngles = []
        self._tigVec = []

    def generatePoints(self):
        xy = [[np.random.uniform(0, 100), np.random.uniform(0, 100)] for _ in range(self._num)]
        self._tigXY = xy

    def generateTigers(self):
        a = np.array([np.random.uniform(4, 8) for _ in range(self._num)])
        b = np.array([np.random.uniform(2, 3.5) for _ in range(self._num)])
        c = np.sqrt(np.square(a) - 0.25 * np.square(b))

        x, y = np.array(list(zip(*self._tigXY))[0]), np.array(list(zip(*self._tigXY))[1])
        x1, y1 = x, y + 0.6 * c
        x2, y2 = x - 0.5 * b, y - 0.4 * c
        x3, y3 = x + 0.5 * b, y - 0.4 * c
        allXY = np.stack((x1, y1, x2, y2, x3, y3), axis=1)
        xy = [xyN.reshape((3, 2)) for xyN in allXY]

        angles = np.random.uniform(0, 2 * np.pi, size=np.size(x))

        for angle in angles:
            self._tigVec.append([-np.sin(angle), -np.cos(angle)])

        rot = np.empty_like(xy)
        for i, angle in enumerate(angles):
            rot[i][0] = rotate(xy[i][0], x[i], y[i], angles[i])
            rot[i][1] = rotate(xy[i][1], x[i], y[i], angles[i])
            rot[i][2] = rotate(xy[i][2], x[i], y[i], angles[i])

        self._tigAngles = angles
        self._tigVert3XY = rot
        self._tigVertAllXY = np.concatenate(rot)

    def addMove(self):
        for i in range(np.shape(self._tigVert3XY)[0]):
            self._tigVert3XY[i][0] = np.add(self._tigVert3XY[i][0], self._tigVec[i])
            self._tigVert3XY[i][1] = np.add(self._tigVert3XY[i][1], self._tigVec[i])
            self._tigVert3XY[i][2] = np.add(self._tigVert3XY[i][2], self._tigVec[i])

            self._tigXY[i] = np.add(self._tigXY[i], self._tigVec[i])

        self._tigVertAllXY = np.concatenate(self._tigVert3XY)

    def changeDir(self, lineHull):
        for i in range(np.shape(self._tigVert3XY)[0]):
            xy1 = [[self._tigVert3XY[i][1][0], self._tigVert3XY[i][1][1]],
                   [self._tigVert3XY[i][2][0], self._tigVert3XY[i][2][1]]]
            line1xy1 = Path(xy1)

            xy2 = [[self._tigVert3XY[i][2][0], self._tigVert3XY[i][2][1]],
                   [self._tigVert3XY[i][0][0], self._tigVert3XY[i][0][1]]]
            line1xy2 = Path(xy2)

            xy3 = [[self._tigVert3XY[i][0][0], self._tigVert3XY[i][0][1]],
                   [self._tigVert3XY[i][1][0], self._tigVert3XY[i][1][1]]]
            line1xy3 = Path(xy3)

            for j in range(np.shape(lineHull)[0] - 1):
                xyH = [lineHull[j], lineHull[j + 1]]
                line2xyH = Path(xyH)

                col1 = line1xy1.intersects_path(line2xyH)
                col2 = line1xy2.intersects_path(line2xyH)
                col3 = line1xy3.intersects_path(line2xyH)

                if col1 or col2 or col3:
                    self._tigVert3XY[i][0] = np.subtract(self._tigVert3XY[i][0], 4 * np.array(self._tigVec[i]))
                    self._tigVert3XY[i][1] = np.subtract(self._tigVert3XY[i][1], 4 * np.array(self._tigVec[i]))
                    self._tigVert3XY[i][2] = np.subtract(self._tigVert3XY[i][2], 4 * np.array(self._tigVec[i]))
                    self._tigXY[i] = np.subtract(self._tigXY[i], 4 * np.array(self._tigVec[i]))
                    self._tigVertAllXY = np.concatenate(self._tigVert3XY)

                    self._tigVert3XY[i][0] = rotate(self._tigVert3XY[i][0], self._tigXY[i][0], self._tigXY[i][1], np.pi)
                    self._tigVert3XY[i][1] = rotate(self._tigVert3XY[i][1], self._tigXY[i][0], self._tigXY[i][1], np.pi)
                    self._tigVert3XY[i][2] = rotate(self._tigVert3XY[i][2], self._tigXY[i][0], self._tigXY[i][1], np.pi)
                    self._tigAngles[i] -= np.pi
                    self._tigVec[i] = [-np.sin(self._tigAngles[i]), -np.cos(self._tigAngles[i])]

                    break

    def checkEnd(self, lineHull):
        np.append(lineHull, [lineHull[0]], axis=0)
        polyLine = Path(lineHull)

        if np.all(polyLine.contains_points(self._tigXY)):
            return True

        for i in range(np.shape(self._tigVert3XY)[0]):
            col1 = polyLine.contains_points([self._tigVert3XY[i][0]])
            col2 = polyLine.contains_points([self._tigVert3XY[i][1]])
            col3 = polyLine.contains_points([self._tigVert3XY[i][2]])

            if ~col1 and ~col2 and ~col3:
                return False

        return True

    def getPoints(self):
        return self._tigXY

    def getTigersVert3XY(self):
        return self._tigVert3XY

    def getTigersVertAllXY(self):
        return self._tigVertAllXY

    def getTigersAngles(self):
        return self._tigAngles


def rotate(x, x_r, y_r, phi):
    return np.array([np.cos(phi) * (x[0] - x_r) + np.sin(phi) * (x[1] - y_r) + x_r,
                     -np.sin(phi) * (x[0] - x_r) + np.cos(phi) * (x[1] - y_r) + y_r])


def jarvisAlg(i, zooMove):
    if i < 2:
        return tigLine, tigersPoints

    notEndJarvis = True

    if np.shape(tigLine.get_xydata())[0] > 2 and zooMove.checkEnd(tigLine.get_xydata()):
        tigLineX.append(tigLine.get_xydata()[0][0])
        tigLineY.append(tigLine.get_xydata()[0][1])
        tigLine.set_data(tigLineX[1:], tigLineY[1:])

        notEndJarvis = False

    zooMove.addMove()
    zooMove.changeDir(tigLine.get_xydata())

    if notEndJarvis:
        tigVert = zoo.getTigersVertAllXY()
        p_i2 = np.array([tigLineX[i - 2], tigLineY[i - 2]])
        p_i1 = np.array([tigLineX[i - 1], tigLineY[i - 1]])
        newP = max(tigVert, key=lambda p_i: angle3Points(p_i, p_i1, p_i2))

        tigLineX.append(newP[0])
        tigLineY.append(newP[1])

    tigLine.set_data(tigLineX[1:], tigLineY[1:])
    tigersXz, tigersYz = list(list(zip(*zooMove.getPoints()))[0]), list(list(zip(*zooMove.getPoints()))[1])
    tigersPoints.set_data(tigersXz, tigersYz)

    for j, newPolygon in enumerate(triangles):
        newPolygon.set_xy(zooMove.getTigersVert3XY()[j])

    return tigLine, tigersPoints


def angle3Points(point1, point2, point3):
    vec1, vec2 = point2 - point1, point3 - point2

    angle1 = np.arctan2(vec1[1], vec1[0])
    angle2 = np.arctan2(vec2[1], vec2[0])
    angle = angle2 - angle1

    if angle < 0:
        angle += 2*np.pi

    return angle


N = 25
zoo = Tigers(N)
zoo.generatePoints()
zoo.generateTigers()
tigers = zoo.getPoints()
tigersVert3XY = zoo.getTigersVert3XY()
tigersVertAllXY = zoo.getTigersVertAllXY()

fig = plt.figure()
ax = plt.axes(xlim=(-10, 110), ylim=(-10, 110))
ax.set_aspect('equal')

tigersX, tigersY = list(list(zip(*tigers))[0]), list(list(zip(*tigers))[1])
tigersPoints, = plt.plot(tigersX, tigersY, 'ro', markersize=0.5)

p1 = min(tigersVertAllXY, key=lambda point: point[1])
p0 = [-10, p1[1]]
tigLineX, tigLineY = [p0[0], p1[0]], [p0[1], p1[1]]
tigLine, = ax.plot(tigLineX[1:], tigLineY[1:], '--bo', markersize=1, linewidth=0.5)

triangles = [Polygon(tigerTri, facecolor='orange', hatch='///////') for tigerTri in tigersVert3XY]
for triangle in triangles:
    ax.add_patch(triangle)

animate = FuncAnimation(fig, func=jarvisAlg, fargs=(zoo, ), frames=N*N, interval=500, repeat=False)

plt.show()
