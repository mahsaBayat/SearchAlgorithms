import sys

from algorithms import A, BFS, DFS, GS, HillClimb, IDS


# Check command line arguments
if len(sys.argv) != 3:
    print('Usage: python ThreeDigits.py <algorithm> <file>')
    exit(1)

algorithm = sys.argv[1]
filepath = sys.argv[2]

# Check algorithm is valid
if algorithm not in ('B', 'D', 'I', 'G', 'A', 'H'):
    print('Invalid algorithm. Choose from: B, D, I, G, A, H')
    exit(1)

# Check file exists
try:
    data = open(filepath, 'rU').readlines()
except FileNotFoundError as ex:
    print('Invalid file. Error: {0}'.format(ex))

# z.fill(3) pads zero by zero 3 times
start = str(data[0]).zfill(3).replace("\n", "")
goal = str(data[1]).zfill(3).replace("\n", "")

# Check if any forbidden nodes are given in the input file.
if len(data) == 3:
    global forbiddenList
    # Split the last line of the input file by commas and store in a list.
    forbiddenList = str(data[2]).split(',')

    # Get rid of the \n in the final element of the list.
    forbiddenList = [s.rstrip() for s in forbiddenList]

else:
    forbiddenList = []


##############################################################################################################################

if algorithm == 'B':
    BFS(start, goal)
elif algorithm == 'D':
    DFS(start, goal)
elif algorithm == 'I':
    IDS(start, goal)
elif algorithm == 'G':
    GS(start, goal)
elif algorithm == 'A':
    A(start, goal)
elif algorithm == 'H':
    HillClimb(start, goal)
