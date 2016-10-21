
import os, time

from readwrite import *
from solver import *
from verifier import *
from plotter import *

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



def solveAllTheThings(skip=False):

    for fileName in os.listdir("group_inputs"):
        if fileName.endswith(".txt"):
            print("Starting on " + fileName)
            if skip:
                currentScore, currentSet = getSolutionVals("solutions/solution-"+fileName.lstrip("group_inputs/input_"))
                if currentScore:
                    print("Solution for {} already exists. Skipping.".format(fileName))
                else:
                    solveFile("group_inputs/"+str(fileName))
            else:
                solveFile("group_inputs/"+str(fileName))

def verifyAllTheThings():

    n,k,points = getValsFromTxt("toughSample.txt")

    for fileName in os.listdir("group_outputs"):
        if fileName.endswith(".txt"):
            # print("Starting on " + fileName)
            try:
                if verifySolution(k, points,"group_outputs/"+fileName):
                    print("{} was good".format(fileName))
                else:
                    print("{} was bad".format(fileName))
            except Exception as e:
                print("{} crashed because of {}".format(fileName, e))

# def testing():

    # print("testing")
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

solveAllTheThings()
verifyAllTheThings()