import itertools

import random

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def getValsFromTxt(fileName):
    """
    Returns n, k and a list of points from a file
    """
    fo = open(fileName, "r")
    lines = fo.readlines()
    fo.close()
    n = int(lines[0])
    k = int(lines[1])
    points = lines[2:]
    pointList = []
    for point in points:
        p = [int(val) for val in point.rstrip('\n').split(" ")]
        pointList.append(p)
    
    return int(n), int(k), pointList


def genSample(fileName):
    """
    Generates sample problem and input file
    """
    n = random.randint(3,1000)
    k = random.randint(2,20)
    points = [str(random.randint(-1000,1000))+ " " + str(random.randint(-1000,1000)) + " " + str(random.randint(-1000,1000)) + "\n" for i in range(n)]

    linesToPrint = [str(n) + "\n"] + [str(k) + "\n"] + points

    fo = open(fileName, "w")
    fo.writelines(linesToPrint)
    fo.close()

def genOutVals(filename, distance, pointSets):
    """
    Creates output file with provided results
    """
    pointLines = [" ".join(map(lambda x: str(x+1),point)) for point in pointSets]
    lines = [distance] + pointLines
    linesToPrint = [str(l)+"\n" for l in lines]
    
    fo = open(filename, "w")
    fo.writelines(linesToPrint)
    fo.close()

def getSolutionVals(fileName):
    """
    Gets the best score and set from a file
    """
    fo = open(fileName, "r")
    lines = fo.readlines()
    fo.close()
    bestScore = int(lines[0])
    bestSet = []
    sets = lines[1:]
    for set in sets:
        p = [int(val)-1 for val in set.rstrip('\n').split(" ")]
        bestSet.append(p)
    return bestScore, bestSet

def verifySolution(k, points, filename):
    """
    Checks whether the solution provided in file is valid for points
    """
    solutionScore, solutionSet = getSolutionVals(filename)
    ## TODO: need to check whether a point was used twice 
    return solutionScore == getSetsScore(points, solutionSet) and len(solutionSet) == k

def verifyInputOutputFileCombination(inputFile, outputFile):
    """
    Checks whether an output file provides a valid solution for an input file
    """
    inputN, inputK, inputPoints = getValsFromTxt(inputFile)
    return verifySolution(inputK, inputPoints, outputFile)


def getManhattan(pOne, pTwo):
    """
    Returns the Manhattan Distance between two points
    """
    return abs(pOne[0] - pTwo[0]) + abs(pOne[1] - pTwo[1]) + abs(pOne[2] - pTwo[2])

def getMaxManhattan(allPoints, indexes):
    """
    Returns the maximum Manhattan Distance between each 2 point combination in a subset of all points
    """
    maxManhattan = 0
    points = [allPoints[i] for i in indexes]
    combs = itertools.combinations(points,2)
    for combination in combs:
        dist = getManhattan(combination[0], combination[1])
        if dist > maxManhattan:
            maxManhattan = dist
    return maxManhattan

def getSetsScore(points,sets):
    """
    Returns the score of sets of point groups
    (The maximum Manhattan Distance between each 2 point combination in each subset)
    """
    maxDistance = 0
    for set in sets:
        dist = getMaxManhattan(points, set)
        if dist > maxDistance:
            maxDistance = dist
    return maxDistance

def randomAlg(n,k,points):
    """
    A random algorithm for determining the sets of points to give the minMax
    Uses the same subset length for all subsets
    Returns the sets of points
    """
    p = list(range(n))
    random.shuffle(p)
    sets = []
    for i in range(k):
        if i == k-1:
            sets.append(p[int(i*(n/k)):])
        else:
            sets.append(p[int(i*(n/k)):int(i*(n/k) + (n/k))])
    return sets




def useAlgorithm(algorithm, n, k, points, runs):
    """
    A way to run an algorithm several times and get the best run score and best set
    """
    bestScore = 100000000
    bestSet = []
    for i in range(runs):
        thisSet = algorithm(n,k,points)
        thisScore = getSetsScore(points, thisSet)
        if thisScore < bestScore:
            bestScore = thisScore
            bestSet = thisSet
    return bestScore, bestSet


def plotSolutionSet(points, set):
    """
    Plot the points of each set with the same color on a 3d graph
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = [0] * len(points)

    for i in range(len(set)):
        for j in range(len(set[i])):
            colors[set[i][j]] = i
    m = "o"

    ax.scatter(xs, ys, zs, c=colors, marker=m)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()




def testing():

    ######
    ## Spec Example
    ######

    # # Get values from the spec sample
    # n, k, points = getValsFromTxt("SpecSample.txt")

    # # Run algorithm for spec sample
    # bestScore, bestSet = useAlgorithm(randomAlg, n, k, points, 100)

    # Plot the sample sets
    plotSolutionSet(points, bestSet)

    # # Print output of spec sample to a file
    # genOutVals("SpecSampleSolution.txt",bestScore, bestSet)

    ######
    ## Generated Sample
    ######

    # Generate a sample input file then get its values and solve it and output the result in a file
    genSample("mySample.txt")
    sampleN, sampleK, samplePoints = getValsFromTxt("mySample.txt")
    sampleScore, sampleSet = useAlgorithm(randomAlg, sampleN, sampleK, samplePoints, sampleN + 300)
    # genOutVals("mySampleSolution.txt",sampleScore, sampleSet)

    # # Verify solution given k and points
    # if verifySolution(sampleK, samplePoints, "mySampleSolution.txt"):
    #     print("That's a valid solution!")
    # else:
    #     print("Invalid solution!")

    # # Verify solution given 2 files
    # if verifyInputOutputFileCombination("mySample.txt", "mySampleSolution.txt"):
    #     print("That's a valid solution!")
    # else:
    #     print("Invalid solution!")

    plotSolutionSet(samplePoints, sampleSet)

testing()

