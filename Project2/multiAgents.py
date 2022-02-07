# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostPos = successorGameState.getGhostPositions()

        xy = newPos
        foodList = newFood.asList()

        values = []
        for goal in foodList:
            values.append(abs(xy[0] - goal[0]) + abs(xy[1] - goal[1]))    #manhattan distance

        
        for ghost in ghostPos:
            v = abs(xy[0] - ghost[0]) + abs(xy[1] - ghost[1]) 
            if v <= 1:   # ghost too close(1 block)
                return -5000        # very bad value that fits this problem 

        if values != []:
            # we divide 10 with min manhattan values to distinguish the better positions
            # we could put any constant value in the place of 10
            weight = 10/min(values)       
        
            return successorGameState.getScore() + weight

        else:
            return successorGameState.getScore() 


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        pacmanIndex = 0

        action = "Stop"
        maximum = float('-inf')
        for act in gameState.getLegalActions(pacmanIndex):
            minmaxValue = self.minimax(gameState.generateSuccessor(pacmanIndex, act), 1, 0)

            if minmaxValue > maximum:
                maximum = minmaxValue
                action = act        # keep best action minimax has given

        return action


    def minimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:      # end minimax
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1

        values = []
        if agentIndex == 0:         # pacman(max)
            for act in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, act)

                values.append(self.minimax(successorGameState, nextAgentIndex, depth))   #recursion
            
            return max(values)

        else:                       # ghosts(min)
            if gameState.getNumAgents() == nextAgentIndex:  # finished agents at this depth
                nextAgentIndex = 0      # to check pacman again
                depth += 1              # increasing depth

            for act in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, act)

                values.append(self.minimax(successorGameState, nextAgentIndex, depth))   #recursion
            
            return min(values)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        pacmanIndex = 0

        action = "Stop"
        maximum = float('-inf')
        a = float('-inf')
        b = float('inf')
        for act in gameState.getLegalActions(pacmanIndex):
            alphaBetaValue = self.alphaBeta(gameState.generateSuccessor(pacmanIndex, act), 1, 0, a, b)

            if alphaBetaValue > maximum:
                maximum = alphaBetaValue
                action = act        # keep best action minimax has given

            if maximum > b:
                return maximum
            a = max(a,maximum)

        return action


    def alphaBeta(self, gameState, agentIndex, depth, a, b):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:      # end minimax
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1

        values = []
        if agentIndex == 0:         # pacman(max)
            for act in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, act)

                value = self.alphaBeta(successorGameState, nextAgentIndex, depth, a, b)   #recursion
                values.append(value)

                if value > b:
                    return value

                a = max(value,a)

            return max(values)

        else:                       # ghosts(min)
            if gameState.getNumAgents() == nextAgentIndex:  # finished agents at this depth
                nextAgentIndex = 0      # to check pacman again
                depth += 1              # increasing depth

            for act in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, act)

                value = self.alphaBeta(successorGameState, nextAgentIndex, depth, a, b)   #recursion
                values.append(value)

                if value < a:
                    return value

                b = min(value,b)
            
            return min(values)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        pacmanIndex = 0

        action = "Stop"
        maximum = float('-inf')
        for act in gameState.getLegalActions(pacmanIndex):
            expectimaxValue = self.expectimax(gameState.generateSuccessor(pacmanIndex, act), 1, 0)

            if expectimaxValue > maximum:
                maximum = expectimaxValue
                action = act        # keep best action minimax has given

        return action


    def expectimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:      # end minimax
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1

        values = []
        if agentIndex == 0:         # pacman(max)
            for act in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, act)

                values.append(self.expectimax(successorGameState, nextAgentIndex, depth))   #recursion
            
            return max(values)

        else:                       # ghosts(min)
            if gameState.getNumAgents() == nextAgentIndex:  # finished agents at this depth
                nextAgentIndex = 0      # to check pacman again
                depth += 1              # increasing depth

            for act in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, act)

                values.append(self.expectimax(successorGameState, nextAgentIndex, depth))   #recursion
            
            return sum(values)/len(actions)     # take average of values


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
      Some calculations in the algorithm are result of trial and error.
      Autograder gives this question 1227.8 average score and 6/6.

     The written function evaluates the given state, finding the closest food
    and searching the ghosts positions. If a ghost is scared it's better to be
    close so pacman can eat it. Respectively if a ghost isn't scared it's better
    to not be close so pacman will not be eaten. 

    """
    "*** YOUR CODE HERE ***"

    evaluation = currentGameState.getScore()


    # calculate evaluation based on the ghosts positions
    xy = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()

    for ghost in ghostStates:
        ghostPos = ghost.getPosition()
        v = abs(xy[0] - ghostPos[0]) + abs(xy[1] - ghostPos[1])       #manhattan distance

        if ghost.scaredTimer:   # ghost is scared
            # we want pacman to eat scared ghosts because it gives good score
            if v <= 2:      # if scared ghost is near increase evaluation
                evaluation += 10/v + 5
            else:
                evaluation += 10/v + 2

        else:                   # normal ghost
            if v <= 1:   # ghost too close(1 block)
                return -5000        # very bad value

            if v <= 3:     # if normal ghost is near decrease evaluation
                evaluation -= 10/v + 5


    # find closest food with manhattan distance
    foodList = currentGameState.getFood().asList()
    values = []
    for goal in foodList:
        values.append(abs(xy[0] - goal[0]) + abs(xy[1] - goal[1]))    #manhattan distance

    if values != []:
        evaluation += 10/min(values)


    return evaluation
    

# Abbreviation
better = betterEvaluationFunction
