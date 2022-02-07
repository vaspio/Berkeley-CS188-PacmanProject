# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    
    start = (problem.getStartState(), "start", 0)
    
    stack = util.Stack()
    stack.push(start) 
    visited = set()     # set of visited nodes
    visited.add(start[0])   # visited keeps only state coordinates

    curstate = start
    parentdict = {}

    while stack.list:

        curstate = stack.pop()

        if problem.isGoalState(curstate[0]): break     # found goal state
       
        visited.add(curstate[0])
        successorList = problem.getSuccessors(curstate[0])
        for i in successorList:             # traverse successors

            if i[0] not in visited:         # ignore if successor state is in visited 
                stack.push(i)
                parentdict[i] = curstate    # keep neighbor states


    # inspiration for using a dictionary from user:amit at 
    # stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search
    path = []
    while curstate != start : # until it reaches the end   

        path.append(curstate[1])        # take directions only
        curstate = parentdict[curstate]

    path.reverse()      # reverse because path begins from goal state

    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    start = (problem.getStartState(), "start", 0)
    
    queue = util.Queue()
    queue.push(start) 
    visited = set()     # set of visited nodes

    parentdict = {}

    while queue.list:
        curstate = queue.pop()    #checking current state

        if problem.isGoalState(curstate[0]): break 

        if curstate[0] not in visited:
            visited.add(curstate[0])
            successorList = problem.getSuccessors(curstate[0])

            for i in successorList: 
                if i[0] not in visited:
                    queue.push(i) 
                    parentdict[i] = curstate 


    path = []
    while curstate != start : # until it reaches the end   

        path.append(curstate[1])        # take directions only
        curstate = parentdict[curstate]

    path.reverse()      # reverse because path begins from goal state

    return path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    import heapq

    start = (problem.getStartState(), "start", 0)
    
    priorityQueue = util.PriorityQueue()
    priorityQueue.push(start,start[2]) 
    visited = set()     # set of visited nodes
    parentdict = {}

    while priorityQueue.heap:

        (cost, _, curstate) = heapq.heappop(priorityQueue.heap)     # pop the item and take its priority(cost)

        if problem.isGoalState(curstate[0]): break 


        if curstate[0] not in visited:
            visited.add(curstate[0])
            successorList = problem.getSuccessors(curstate[0])

            for i in successorList:             # traverse successors

                if i[0] not in visited:         # ignore if successor state visited 
                    priorityQueue.update(i, i[2]+cost)

                    if i in parentdict:
                        _,c = parentdict.get(i)
                        if c > cost:        # keep path of lower cost
                            parentdict[i] = (curstate,cost) 
                    else:
                        parentdict[i] = (curstate,cost)     


    path = []
    while curstate != start : # until it reaches the end   

        path.append(curstate[1])        # take directions only
        curstate,cost = parentdict[curstate]

    path.reverse()      # reverse because path begins from goal state

    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    import heapq

    start = (problem.getStartState(), "start", 0)
    
    priorityQueue = util.PriorityQueue()
    priorityQueue.push(start,start[2]) 
    visited = set()         # set of visited nodes
    parentdict = {}
    realCost = {}
    realCost[start] = 0     # keep path cost without heuristic

    while priorityQueue.heap:

        curstate = priorityQueue.pop()

        if problem.isGoalState(curstate[0]): break 

        if curstate[0] not in visited:
            visited.add(curstate[0])
            successorList = problem.getSuccessors(curstate[0])

            for i in successorList:
                newCost = i[2]+realCost[curstate]       # calculate new real cost
                if i not in realCost or newCost < realCost[i]:      # if successor dont have a path stored or new path cost less than before
                    realCost[i] = newCost
                    priorityQueue.update(i, newCost + heuristic(i[0],problem))  # update with cost+heuristic as priority 

                    parentdict[i] = curstate
        

    path = []
    while curstate != start : # until it reaches the end   

        path.append(curstate[1])        # take directions only
        curstate = parentdict[curstate]

    path.reverse()      # reverse because path begins from goal state

    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
