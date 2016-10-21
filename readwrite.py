
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
            p = [int(val)-1 for val in set.rstrip('\n').rstrip("\r").rstrip(" ").split(" ")]
            bestSet.append(p)
        return bestScore, bestSet
    except:
        return False, False

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