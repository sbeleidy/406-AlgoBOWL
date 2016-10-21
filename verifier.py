


def verifySolution(k, points, filename):
    """
    Checks whether the solution provided in file is valid for points
    """
    solutionScore, solutionSet = getSolutionVals(filename)
    if solutionScore:
        ## TODO: need to check whether a point was used twice
        actualScore = getSetsScore(points, solutionSet)
        if solutionScore == actualScore and len(solutionSet) == k:
            return True
        else:
            print("{} Solution provided: {}, actual: {}".format(filename,solutionScore,actualScore))
            return False
    else:
        print("Error reading file {}".format(filename))

def verifyInputOutputFileCombination(inputFile, outputFile):
    """
    Checks whether an output file provides a valid solution for an input file
    """
    inputN, inputK, inputPoints = getValsFromTxt(inputFile)
    return verifySolution(inputK, inputPoints, outputFile)
