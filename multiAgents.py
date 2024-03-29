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
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        # print(newPos)
        # print(newFood)
        # print(newGhostStates)
        # print(newScaredTimes)

        # make is so that if it is closer to a ghost then reduce the score
        # increase if closer to food

        # only one ghost in classic map
        ghost_pos = newGhostStates[0].getPosition()
        nearest_ghost_dist = manhattanDistance(ghost_pos, newPos)

        # nearest food
        all_food_pos = newFood.asList()
        score = successorGameState.getScore()

        if len(all_food_pos) and nearest_ghost_dist:
            nearest_food_dist = min([manhattanDistance(
                foodPos, newPos) for foodPos in all_food_pos])
            score = score - (5 / nearest_ghost_dist) + (10 / nearest_food_dist)

        "*** YOUR CODE HERE ***"
        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        # Use function for min and max of node
        # need same args to call main_delegation again after agents turn
        # mechanism to keep track with agenCount whether ghost or pacman
        INF, NEG_INF = float("inf"), -float("inf")

        def min_recurse(depth, agentCount, gameState):
            # action value pair
            best_action = ""
            best_value = INF
            node_actions = gameState.getLegalActions(agentCount)
            # base
            if not node_actions:
                # print(self.depth)
                return self.evaluationFunction(gameState)

            for successor in node_actions:
                curr_succ = gameState.generateSuccessor(agentCount, successor)

                value_node = main_delegation(depth, agentCount + 1, curr_succ)
                
                if type(value_node) is list:
                    updated_action = value_node[1]
                else: 
                    updated_action = value_node
                # update best_action
                if updated_action < best_value:
                    best_action = successor
                    best_value = updated_action
            return [best_action, best_value]

        def max_recurse(depth, agentCount, gameState):
            # action value pair
            best_action = ""
            best_value = NEG_INF
            node_actions = gameState.getLegalActions(agentCount)

            # base
            if not node_actions:
                # print(self.depth)
                return self.evaluationFunction(gameState)

            for successor in node_actions:
                curr_succ = gameState.generateSuccessor(agentCount, successor)

                value_node = main_delegation(depth, agentCount + 1, curr_succ)
                
                if type(value_node) is list:
                    updated_action = value_node[1]
                else: 
                    updated_action = value_node
                # update best_action
                if updated_action > best_value:
                    best_action = successor
                    best_value = updated_action
            return [best_action, best_value]

            
        # main recurring function depending on who the player is
        def main_delegation(depth, agentCount, gameState):
            # see if all ghosts or agent recursed this time
            iterAgentCount = gameState.getNumAgents()
            if iterAgentCount <= agentCount:
                agentCount = 0
                depth += 1
            
            # stopping mechanisms
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentCount == 0:
                return max_recurse(depth, agentCount, gameState)
            else: 
                return min_recurse(depth, agentCount, gameState)
        
        return main_delegation(0, 0, gameState)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        INF, NEG_INF = float("inf"), -float("inf")

        def min_recurse(depth, agentCount, gameState, alpha, beta):
            # action value pair
            best_action = ""
            best_value = INF
            node_actions = gameState.getLegalActions(agentCount)
            # base
            if not node_actions:
                # print(self.depth)
                return self.evaluationFunction(gameState)

            for successor in node_actions:
                curr_succ = gameState.generateSuccessor(agentCount, successor)

                value_node = main_delegation(depth, agentCount + 1, curr_succ, alpha, beta)
                
                if type(value_node) is list:
                    updated_action = value_node[1]
                else: 
                    updated_action = value_node
                # update best_action
                if updated_action < best_value:
                    best_action = successor
                    best_value = updated_action
                
                # pruning
                if updated_action < alpha:
                    return [successor, updated_action]
                
                beta = min([beta, updated_action])
            return [best_action, best_value]

        def max_recurse(depth, agentCount, gameState, alpha, beta):
            # action value pair
            best_action = ""
            best_value = NEG_INF
            node_actions = gameState.getLegalActions(agentCount)

            # base
            if not node_actions:
                # print(self.depth)
                return self.evaluationFunction(gameState)

            for successor in node_actions:
                curr_succ = gameState.generateSuccessor(agentCount, successor)

                value_node = main_delegation(depth, agentCount + 1, curr_succ, alpha, beta)
                
                if type(value_node) is list:
                    updated_action = value_node[1]
                else: 
                    updated_action = value_node
                # update best_action
                if updated_action > best_value:
                    best_action = successor
                    best_value = updated_action

                # pruning
                if updated_action > beta:
                    return [successor, updated_action]

                alpha = max([alpha, updated_action])
            return [best_action, best_value]

            
        # main recurring function depending on who the player is
        def main_delegation(depth, agentCount, gameState, alpha, beta):
            # see if all ghosts or agent recursed this time
            iterAgentCount = gameState.getNumAgents()
            if iterAgentCount <= agentCount:
                agentCount = 0
                depth += 1
            
            # stopping mechanisms
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentCount == 0:
                return max_recurse(depth, agentCount, gameState, alpha, beta)
            else: 
                return min_recurse(depth, agentCount, gameState, alpha, beta)
        
        return main_delegation(0, 0, gameState, NEG_INF, INF)[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def max_recurse(self, gameState, depth):
        node_actions = gameState.getLegalActions(0)

        if not node_actions:
            return self.evaluationFunction(gameState), None
        if depth > self.depth or gameState.isWin():
            return self.evaluationFunction(gameState), None

        costs = []
        for successor in node_actions:
            curr_succ = gameState.generateSuccessor(0, successor)
            costs.append((self.expected_recurse(curr_succ, 1, depth)[0], successor))
        return max(costs)
    
    def expected_recurse(self, gameState, agentCount, depth):
        node_actions = gameState.getLegalActions(agentCount)

        if not node_actions:
            return self.evaluationFunction(gameState), None
        if gameState.isLose():
            return self.evaluationFunction(gameState), None

        costs = []
        for successor in node_actions:
            curr_succ = gameState.generateSuccessor(agentCount, successor)
            
            iterAgents = gameState.getNumAgents() - 1
            if iterAgents == agentCount:
                costs.append(self.max_recurse(curr_succ, depth + 1))
            else: 
                costs.append(self.expected_recurse(curr_succ, agentCount + 1, depth))

        # calculating averages for optimization
        sum_costs = map(lambda x: float(x[0]) / len(costs), costs)
        return sum(sum_costs), None

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        result = self.max_recurse(gameState, 1)
        return result[1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ghostStates = currentGameState.getGhostStates()
    totalScore = currentGameState.getScore()
    pacPos = currentGameState.getPacmanPosition()
    all_food = currentGameState.getFood().asList()

    # find the furthest food distance to make it reach that pellet faster
    all_dist = [1.0 / manhattanDistance(foodPos, pacPos) for foodPos in all_food]
    # for last state
    all_dist.append(0) 

    return max(all_dist) + totalScore
    


# Abbreviation
better = betterEvaluationFunction
