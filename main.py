import itertools

import random

import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt

import os

import time

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
        p = [int(val) for val in point.rstrip('\n').rstrip(" ").split(" ")]
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
    [set.sort() for set in pointSets]
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
    try:
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
    except:
        return False, False

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

#def toughSolution(n, k, points):
#    for point in points:
#        if point[0] >500 and point[1] > 500


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

def selectRandomStartingPoints(points, k):
    return random.sample(range(len(points)), k)

def selectRandomStartingCoords(points, k):
    return random.sample(points, k)

def selectGoodStartingCoords(k, r=False):
    goodPoints = [
        [500, 500, 500],
        [-500, -500, -500],
        [0, 0, 0],
        [500, 0 ,500],
        [500, 500, 0],
        [0, 500, 500],
        [-500, 0 ,-500],
        [-500, -500, 0],
        [0, -500, -500],
        [0, 0, 500],
        [0, 500, 0],
        [500, 0, 0],
        [0, 0, -500],
        [0, -500, 0],
        [-500, 0, 0],
        [750, 750, 750],
        [-750, -750, -750],
        [750, 0, 750],
        [750, 750, 0],
        [0, 750, 750],
        [750, 0, 0],
        [0, 750, 0],
        [0, 0, 750],
        [-750, 0, -750],
        [-750, -750, 0],
        [0, -750, -750],
        [-750, 0, 0],
        [0, -750, 0],
        [0, 0, -750],
        [250, 250, 250],
        [-250, -250, -250],
        [250, 0, 250],
        [250, 250, 0],
        [0, 250, 250],
        [250, 0, 0],
        [0, 250, 0],
        [0, 0, 250],
        [-250, 0, -250],
        [-250, -250, 0],
        [0, -250, -250],
        [-250, 0, 0],
        [0, -250, 0],
        [0, 0, -250]
    ]
    if r:
        return random.sample(goodPoints,k)
    else:
        return goodPoints[0:k]

def getAllDistancesFromPoint(points, pointIndex):
    return [getManhattan(points[pointIndex], i) for i in points]

def getAllDistancesFromMultiplePoints(points, indexes):
    return [[getManhattan(point, points[index]) for index in indexes ] for point in points]

def getAllDistancesFromCoords(points, coords):
    return [[getManhattan(point, coord) for coord in coords ] for point in points]

def getSetsFromStartingPoints(points, startingIndexes):
    allDistances = getAllDistancesFromMultiplePoints(points, startingIndexes)
    setIndex = [distances.index(min(distances)) for distances in allDistances]

    sets = [[] for i in range(len(startingIndexes))]
    for i in range(len(points)):
        sets[setIndex[i]].append(i)
    return sets

def getSetsFromStartingCoords(points, startingCoords):
    allDistances = getAllDistancesFromCoords(points, startingCoords)
    setIndex = [distances.index(min(distances)) for distances in allDistances]

    sets = [[] for i in range(len(startingCoords))]
    for i in range(len(points)):
        sets[setIndex[i]].append(i)
    return sets

def randomStartingPointAlgorithm(n,k,points):
    start = selectRandomStartingPoints(points, k)
    return getSetsFromStartingPoints(points, start)

def iterateAlgorithm(n,k,points, start, iteratorAlg, iterations):
    bestSets = getSetsFromStartingCoords(points,start)
    bestScore = getSetsScore(points, bestSets)

    newSets = bestSets

    for i in range(iterations):
        start = getNewStart(points, newSets, iteratorAlg)
        newSets = getSetsFromStartingCoords(points, start)
        newScore = getSetsScore(points, newSets)
        if newScore < bestScore:
            bestSets = newSets
            bestScore = newScore

    return bestScore, bestSets

def getNewStart(points, sets, alg):
    start = []
    for aSet in sets:
        if len(aSet) >=2:
            start.append(alg([points[i] for i in aSet]))
    return start


def findGeometricCenter(set):
    xs = [p[0] for p in set]
    ys = [p[1] for p in set]
    zs = [p[2] for p in set]

    minX = min(xs)
    minY = min(ys)
    minZ = min(zs)

    centerX = abs(max(xs) - minX)/2 + minX
    centerY = abs(max(ys) - minY)/2 + minY
    centerZ = abs(max(zs) - minZ)/2 + minZ

    return [centerX, centerY, centerZ]

def findMean(set):
    xs = [p[0] for p in set]
    ys = [p[1] for p in set]
    zs = [p[2] for p in set]

    meanX = sum(xs)/len(xs)
    meanY = sum(ys)/len(ys)
    meanZ = sum(zs)/len(zs)

    return [meanX, meanY, meanZ]


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

def genToughPoint():

    x = random.randint(0,1)
    y = random.randint(0,1)
    z = random.randint(0,1)

    result = {
        '0': lambda x: random.randint(500,1000),
        '1': lambda x: random.randint(-1000,-500)
    }

    return str(result[str(x)](1))+ " " + str(result[str(y)](1)) + " " + str(result[str(z)](1)) + "\n"

def genToughSample(fileName):
    n = 999
    k = 15
    toughPoints = [
        "0 0 0\n","1 1 1\n",
        "500 0 500\n", "501 1 501\n",
        "0 500 500\n", "1 501 501\n",
        "500 500 0\n", "501 501 1\n",
        "-500 0 -500\n", "-501 1 -501\n",
        "0 -500 -500\n", "1 -501 -501\n",
        "-500 -500 0\n", "-501 -501 1\n"
    ]
    generalPoints = [genToughPoint() for i in range(n-len(toughPoints))]

    points = generalPoints + toughPoints

    random.shuffle(points)

    points[-1] = points[-1].rstrip('\n')

    linesToPrint = [str(n) + "\n"] + [str(k) + "\n"] + points

    fo = open(fileName, "w")
    fo.writelines(linesToPrint)
    fo.close()

# genToughSample("toughSample.txt")

def solve(n, k, points):

    bestScore = 10000000
    bestSets = []
    winningAlgorithm = "NA"

    ## General Random Algorithm
    start = time.clock()
    randomScore, randomSets = useAlgorithm(randomAlg, n, k, points, 1000)
    if randomScore < bestScore:
        bestScore = randomScore
        bestSets = randomSets
        winningAlgorithm = "General Random"
    print("General Random took {} seconds".format(str(time.clock() - start)))

    ## Nearest Neighbor Random Start
    start = time.clock()
    nnRandomScore, nnRandomSets = useAlgorithm(randomStartingPointAlgorithm, n, k, points, 1000)
    if nnRandomScore < bestScore:
        bestScore = nnRandomScore
        bestSets = nnRandomSets
        winningAlgorithm = "NN Random Start"
    print("NN Random Start took {} seconds".format(str(time.clock() - start)))

    iteratorAlgorithms = {
        'Mean': findMean,
        'Geometric Center': findGeometricCenter
    }

    for algName in iteratorAlgorithms:
        ## Iterative Nearest Neighbor Random Start
        start = time.clock()
        for i in range(50):
            iterativeRandomScore, iterativeRandomSets = iterateAlgorithm(n, k, points, selectRandomStartingCoords(points, k), iteratorAlgorithms[algName], 100)
            if iterativeRandomScore < bestScore:
                bestScore = iterativeRandomScore
                bestSets = iterativeRandomSets
                winningAlgorithm = "Iterative Random Start - " + algName
        print("Iterative Random Start - {} took {} seconds".format(algName, str(time.clock() - start)))

        ## Iterative Nearest Neighbor Good Start
        start = time.clock()
        iterativeGoodScore, iterativeGoodSets = iterateAlgorithm(n, k, points, selectGoodStartingCoords(k), iteratorAlgorithms[algName], 100)
        if iterativeGoodScore < bestScore:
            bestScore = iterativeGoodScore
            bestSets = iterativeGoodSets
            winningAlgorithm = "Iterative Good Start - " + algName
        print("Iterative Good Start - {} took {} seconds".format(algName, str(time.clock() - start)))

        ## Iterative Nearest Neighbor Random Good Start
        start = time.clock()
        for i in range(10):
            iterativeRandomGoodScore, iterativeRandomGoodSets = iterateAlgorithm(n, k, points, selectGoodStartingCoords(k, True), iteratorAlgorithms[algName], 100)
            if iterativeRandomGoodScore < bestScore:
                bestScore = iterativeRandomGoodScore
                bestSets = iterativeRandomGoodSets
                winningAlgorithm = "Iterative Random Good Start - " + algName
        print("Iterative Random Good Start - {} took {} seconds".format(algName, str(time.clock() - start)))

    return bestScore, bestSets, winningAlgorithm

def solveFile(fileName):
    start = time.clock()
    n, k, points = getValsFromTxt(fileName)
    bestScore, bestSet, winner = solve(n,k,points)

    currentScore, currentSet = getSolutionVals("solutions/solution-"+fileName.lstrip("group_inputs/input_"))

    if currentScore:
        print("Got here")
        if bestScore < currentScore:
            print("New Score Better")
            genOutVals("solutions/solution-"+fileName.lstrip("group_inputs/input_"), bestScore, bestSet)
    else:
        genOutVals("solutions/solution-"+fileName.lstrip("group_inputs/input_"), bestScore, bestSet)

    print("{} was solved with {} in {} seconds.".format(fileName, winner, str(time.clock() - start)))

def plotGroup(n):
    score, sets = getSolutionVals("solutions/solution-"+str(n)+".txt")
    n, k, points = getValsFromTxt("group_inputs/input_group"+str(n)+".txt")
    plotSolutionSet(points, sets)

def solveAllTheThings(skip=False):

    for fileName in os.listdir("group_inputs"):
        if fileName.endswith(".txt"):
            print("Starting on" + fileName)
            if skip:
                currentScore, currentSet = getSolutionVals("solutions/solution-"+fileName.lstrip("group_inputs/input_"))
                if currentScore:
                    print("Solution for {} already exists. Skipping.".format(fileName))
                else:
                    solveFile("group_inputs/"+str(fileName))
            else:
                solveFile("group_inputs/"+str(fileName))

def testing():

    print("testing")
    ######
    ## Spec Example
    ######

    # # Get values from the spec sample
    # n, k, points = getValsFromTxt("SpecSample.txt")

    # # Run algorithm for spec sample
    # bestScore, bestSet = useAlgorithm(randomAlg, n, k, points, 100)

    # # Plot the sample sets
    # plotSolutionSet(points, bestSet)

    # # Print output of spec sample to a file
    # genOutVals("SpecSampleSolution.txt",bestScore, bestSet)

    ######
    ## Generated Sample
    ######

    # # Generate a sample input file then get its values and solve it and output the result in a file
    # genSample("mySample.txt")
    # sampleN, sampleK, samplePoints = getValsFromTxt("mySample.txt")
    # sampleScore, sampleSet = useAlgorithm(randomStartingPointAlgorithm, sampleN, sampleK, samplePoints, sampleN+300)
    # genOutVals("mySampleSolution.txt",sampleScore, sampleSet)
    # plotSolutionSet(samplePoints, sampleSet)

    # iterativeScore, iterativeSet = useAlgorithm(iterativeStartingPointsAlgorithm, sampleN, sampleK, samplePoints, 20)
    # genOutVals("mySampleSolution-Iterative.txt",iterativeScore, iterativeSet)
    # plotSolutionSet(samplePoints, iterativeSet)

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

    # plotSolutionSet(samplePoints, sampleSet)

    # ## Tough sample
    # toughN, toughK, toughPoints = getValsFromTxt("toughSample.txt")
    # toughScore, toughSet = useAlgorithm(randomStartingPointAlgorithm, toughN, toughK, toughPoints, 100)
    # genOutVals("toughSampleSolution.txt",toughScore, toughSet)
    # plotSolutionSet(toughPoints, toughSet)

    # genToughPoint()

# testing()

# solveAllTheThings(skip=True)

# plotGroup(2)
