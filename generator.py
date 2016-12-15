import random


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