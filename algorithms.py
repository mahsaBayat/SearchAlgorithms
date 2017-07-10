import sys
import math
import operator

from operator import attrgetter


SEARCH_LIMIT = 1000


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


###############################################################################################################################

class Node:
    def __init__(self, name, parent, lastMove, manHeur):
        self.name = name
        self.parent = parent
        # Children is a list of objects
        self.children = []
        self.lastMove = lastMove
        self.manHeur = manHeur

    # For debugging purposes.
    def __str__(self):
        if self.parent is None:
            return 'node {0} parent <null> last move {1} manHeur {2}'.format(self.name, self.lastMove, self.manHeur)

        # return 'node {0} parent {1} last move {2}'.format(self.name, self.parent.name, self.lastMove)
        return 'node {0} parent {1} last move {2} manHeur {3}'.format(self.name, self.parent, self.lastMove, self.manHeur)

# Breadth First Search
def BFS(start, goal):

    manHeur = manhattanDistance(start, goal)
    startNode = Node(str(start), None, -1, manHeur)

    # All the expanded node objects will be added here.
    expandedObjects = []
    # All the expanded node names will be added here. This is output line one.
    expandedNames = []
    # All the generated children objects will be in fringe, waiting to be visited.
    fringe = [startNode]

    while (len(expandedObjects) < SEARCH_LIMIT and len(fringe) != 0):

        node = fringe[0]
        fringe.pop(0)

        # Add the first node from fringe to expanded.
        if isIn(node, expandedObjects):
            continue
        else:
            expandedObjects.append(node)

        if str(goal) == node.name:
            for e in expandedObjects:
                expandedNames.append(e.name)
                # print(expandedNames)

            # Output line one
            path = pathFinder(node, [])
            print(path)
            # Output line two
            print(','.join(expandedNames))
            # Now that the goal is found, get out of the loop.
            break


        # Generate children for the popped element from the fringe.
        children = generateChildren(node, goal)

        for child in children:
            fringe.append(child)
    else:
        # Error handling
        print('No solution found.')
        for e in expandedObjects:
            expandedNames.append(e.name)
        print(','.join(expandedNames))

# Depth First Search
def DFS(start, goal):

    manHeur = manhattanDistance(start, goal)
    startNode = Node(str(start), None, -1, manHeur)

    # All the expanded node objects will be added here.
    expandedObjects = []
    # All the expanded node names will be added here. This is output line one.
    expandedNames = []
    # All the generated children objects will be in fringe, waiting to be visited.
    fringe = [startNode]

    while (len(expandedObjects) < SEARCH_LIMIT and len(fringe) != 0):
        node = fringe[0]
        fringe.pop(0)

        # Add the first node from fringe to expanded.
        if isIn(node, expandedObjects):
            continue
        else:
            expandedObjects.append(node)

        if str(goal) == node.name:
            for e in expandedObjects:
                expandedNames.append(e.name)
                # print(expandedNames)

            # Output line one
            path = pathFinder(node, [])
            print(path)
            # Output line two
            print(','.join(expandedNames))
            # Now that the goal is found, get out of the loop.
            break

        # Generate children for the popped element from the fringe.
        children = generateChildren(node, goal)
        # Reverse children to add the left most one to the beginning of the list.
        childrenReversed = list(reversed(children))

        for child in childrenReversed:
            fringe.insert(0, child)

    else:
        # Error handling
        print('No solution found.')
        for e in expandedObjects:
            expandedNames.append(e.name)
        print(','.join(expandedNames))

# Greedy Search:
def GS(start, goal):

    manHeur = manhattanDistance(start, goal)
    startNode = Node(str(start).zfill(3), None, -1, manHeur)

    # All the expanded node objects will be added here.
    expandedObjects = []
    # All the expanded node names will be added here. This is output line one.
    expandedNames = []
    # All the generated children objects will be in fringe, waiting to be visited.
    fringe = [startNode]

    while (len(expandedObjects) < SEARCH_LIMIT and len(fringe) != 0):

        node = fringe[0]
        fringe.pop(0)

        # Add the first node from fringe to expanded.
        if isIn(node, expandedObjects):
            continue
        else:
            expandedObjects.append(node)

        if str(goal) == node.name:
            for e in expandedObjects:
                expandedNames.append(e.name)
                # print(expandedNames)

            # Output line one
            path = pathFinder(node, [])
            print(path)
            # Output line two
            print(','.join(expandedNames))
            # Now that the goal is found, get out of the loop.
            break


        # Generate children for the popped element from the fringe.
        children = generateChildren(node, goal)

        for child in children:
            fringe.insert(0,child)
            # Sorts the fringe list based on the heuristic attribute of its objects.
            fringe.sort(key=operator.attrgetter("manHeur"), reverse=False)
    else:
        # Error handling
        print('No solution found.')
        for e in expandedObjects:
            expandedNames.append(e.name)
        print(','.join(expandedNames))

# A* Search
def A(start, goal):

    manHeur = manhattanDistance(start, goal)
    startNode = Node(str(start).zfill(3), None, -1, manHeur)

    # All the expanded node objects will be added here.
    expandedObjects = []
    # All the expanded node names will be added here. This is output line one.
    expandedNames = []
    # All the generated children objects will be in fringe, waiting to be visited.
    fringe = [startNode]

    while (len(expandedObjects) < SEARCH_LIMIT and len(fringe) != 0):

        node = fringe[0]
        fringe.pop(0)

        # Add the first node from fringe to expanded.
        if isIn(node, expandedObjects):
            continue
        else:
            expandedObjects.append(node)

        if str(goal) == node.name:
            for e in expandedObjects:
                expandedNames.append(e.name)
                # print(expandedNames)

            # Output line one
            path = pathFinder(node, [])
            print(path)
            # Output line two
            print(','.join(expandedNames))
            # Now that the goal is found, get out of the loop.
            break


        # Generate children for the popped element from the fringe.
        children = generateChildren(node, goal)

        for child in children:

            # Returns the path cost from the start node to the current node that's being investigated.
            cost = costCal(node, [])
            # Alter the heuristic value of each child by adding the path cost to it.
            child.manHeur += cost

            fringe.insert(0,child)
            # Sorts the fringe list based on the heuristic attribute of its objects.
            fringe.sort(key=operator.attrgetter("manHeur"), reverse=False)

    else:
        # Error handling
        print('No solution found.')
        for e in expandedObjects:
            expandedNames.append(e.name)
        print(','.join(expandedNames))

# Iterative Deepening Depth First Search
def IDS(start, goal):
    pass

# Depth-limited Search
def DLS(startNode, goal, depth):
    pass

# Hill Climbing
def HillClimb(start, goal):

    manHeur = manhattanDistance(start, goal)
    startNode = Node(str(start).zfill(3), None, -1, manHeur)

    # All the expanded node objects will be added here.
    expandedObjects = []
    # All the expanded node names will be added here. This is output line one.
    expandedNames = []
    # All the generated children objects will be in fringe, waiting to be visited.
    fringe = [startNode]

    temp = []

    while (len(expandedObjects) < SEARCH_LIMIT and len(fringe) != 0):

        # Our current node which is the first element in the fringe list.
        node = fringe[0]
        fringe.pop(0)

        # Check if the node had been expanded before or not.
        if isIn(node, expandedObjects):
            continue
        else:
            # Add the first node from fringe to expanded.
            expandedObjects.append(node)

        if str(goal) == node.name:
            for e in expandedObjects:
                expandedNames.append(e.name)

            # Output line one
            path = pathFinder(node, [])
            print(path)
            # Output line two
            print(','.join(expandedNames))
            # Now that the goal is found, get out of the loop.
            break


        # Generate children for the popped element from the fringe.
        children = generateChildren(node, goal)

        # Store the children in the reversed order.
        temp = list(reversed(children))

        for child in temp:

            # Check if the child's heuristic value is less than ot equals to the
            # heuristic value of the node being investigated.
            if(child.manHeur <= node.manHeur):
                # Get the minimum value among the heuristic value.
                obj = min(temp, key=attrgetter('manHeur'))
                fringe.insert(0, obj)
                # Sorts the fringe list based on the heuristic attribute of its objects.
                fringe.sort(key=operator.attrgetter("manHeur"), reverse=False)

    else:
        # Error handling
        print('No solution found.')
        for e in expandedObjects:
            expandedNames.append(e.name)
        print(','.join(expandedNames))


# Generate children in all the functions above.
def generateChildren(node, goal):

    nodeString = str(node.name).zfill(3) # If all the digits are zero, it pads it 3 times.
    lastMove = node.lastMove
    # Maximum number of children per node is 6.
    for digit in range(0,6):

        # 0,0,1,1,2,2 which are the indexes of nodeString
        index = int(math.floor(digit/2))
        # Defaults to the left-most digit
        currentMove = 0

         # Skips successive moves
        if (index == lastMove):
            continue

        else:
            if (digit % 2 == 0):

                # Skips decrementing 0
                if (int(nodeString[index]) == 0):
                    continue

                newVal = str(int(nodeString[index]) - 1)
                currentMove = index

            else:

                # Skips incrementing 9
                if (int(nodeString[index]) == 9):
                    continue

                newVal = str(int(nodeString[index]) + 1)
                currentMove = index

            # The name attribute of the node object that's being created.
            name = nodeString[:index] + newVal + nodeString[index+1:]

            # Calculate the manHeur for each node that's being created.
            manHeur = manhattanDistance(goal, name)

            # Create a new child object
            child = Node(name, node, currentMove, manHeur)

        # Check if the child is forbidden or not.
        if not checkForbidden(child.name):
            # Update the children attribute of the node object.
            node.children.append(child)

    # The list of all the node objects in the children.
    return node.children

# Find the path for in all the functions above.
def pathFinder(node, path):
    # This is because the start node doesn't have a parent so the returned object is null.
    if (node == None):
        return None
    else:
        path.append(node.name)
        pathFinder(node.parent, path)
        return ','.join(reversed(path))

# Find the Manhattan heuristic value
def manhattanDistance(nodeOne, nodeTwo):

    # In order to iterate through each node digits, first convert it into strings.
    n1 = str(nodeOne).zfill(3) # Padding the zero.
    n2 = str(nodeTwo).zfill(3)
    heuristic = abs(int(n1[0]) - int(n2[0])) + abs(int(n1[1]) - int(n2[1])) + abs(int(n1[2]) - int(n2[2]))
    return heuristic

# Returns True if it's forbidden and False if it's ok.
def checkForbidden(name):
    if name in forbiddenList:
        return True
    return False

# Check if the node being investigated is already expanded or not.
def isIn(node, expanded):

    for expandedNode in expanded:
        if str(node.name) + str(node.lastMove) == str(expandedNode.name) + str(expandedNode.lastMove):
            return True
    return False

# For calculating the path cost
def costCal(node, pathToNode):
    # This is because the start node doesn't have a parent so the returned object is null.
    if (node == None):
        return None
    else:
        pathToNode.append(node.name)
        pathFinder(node.parent, pathToNode)
        return len(pathToNode)
