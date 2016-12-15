import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from readwrite import *

def plotSolutionSet(points, set=None):
    """
    Plot the points of each set with the same color on a 3d graph
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = [0] * len(points)

    if set != None:
        for i in range(len(set)):
            for j in range(len(set[i])):
                colors[set[i][j]] = i

    m = "o"

    ax.scatter(xs, ys, zs, c=colors, marker=m)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

def plotGroup(n):
    score, sets = getSolutionVals("solutions/solution-"+str(n)+".txt")
    n, k, points = getValsFromTxt("group_inputs/input_group"+str(n)+".txt")
    plotSolutionSet(points, sets)