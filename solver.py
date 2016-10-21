import random, itertools, time


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

