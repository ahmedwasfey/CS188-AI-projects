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
def euclideanDistance(xy1 , xy2):
    "Returns the Euclidean distance between points xy1 and xy2"
    return (abs( xy1[0] - xy2[0] )**2 + abs( xy1[1] - xy2[1] )**2)**0.5

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
        if action == 'Stop':
             return -float("inf")
        curPos = currentGameState.getPacmanPosition()
        curGhostsPos = [ghostState.start.pos for ghostState in currentGameState.getGhostStates()]
        curNearstGhost = min ([euclideanDistance(curPos, Gpos) for Gpos in curGhostsPos ])
        curFood = currentGameState.getFood()
        curFoodList = curFood.asList()
        curFoodDis= [(euclideanDistance(curPos , z) , z) for z in curFoodList]
        nearstFood = min(curFoodDis)
        #print( min (curFoodDis))
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostsPos= [ghostState.start.pos for ghostState in newGhostStates]
        newDisFromGhosts = [euclideanDistance(newPos , Gpos) for Gpos in newGhostsPos ]
        newNearstGhost =min(newDisFromGhosts)
        #print (newPos , newScaredTimes , newDisFromGhosts)
        "*** YOUR CODE HERE ***"
        #score_diff = successorGameState.getScore()  - currentGameState.getScore()
        nearsFood_diff = int(nearstFood[0] - euclideanDistance(newPos , nearstFood[1]))
        nearstGhost_diff = int(newNearstGhost - curNearstGhost )
        if newNearstGhost >5 or not max(newScaredTimes) ==0:
            nearstGhost_diff =0
        total_eval = 300+ 5*nearsFood_diff + (7 * nearstGhost_diff ) + successorGameState.getScore()+ max(newScaredTimes)
        if max(newScaredTimes)==0 :
            total_eval = total_eval
        #print (total_eval)
        return  abs(total_eval)

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
    def value (self , gameState ,my_depth , agent ):
        #print(my_depth) 
        if my_depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        if agent == 'min':
            return  self.minv(gameState, my_depth)
        if agent == 'max':
            return self.maxv(gameState , my_depth)
    def maxv (self , gameState,d):
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()
        v= -9999999999
        ans = None
        leg_act = gameState.getLegalActions(0)
        #leg_act.remove('Stop')
        for act in leg_act :
            sucss_state = gameState.generateSuccessor(0 , act)
            v =max(v, self.value(sucss_state,d, 'min')) 
        return v 
    def minv(self , gameState, d  , idx =1 ):
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()
        v = 99999999999
        ans =None       
        leg_act = gameState.getLegalActions(idx)
        for act in leg_act :
            sucss_state = gameState.generateSuccessor(idx , act)
            if idx  +1==gameState.getNumAgents():
               v =min (v, self.value(sucss_state , d+1, 'max'))    
            else :
                v =min (v,self.minv (sucss_state, d , idx+1 ))
        
        return v
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
        legal = gameState.getLegalActions(0)
        ans_act = None 
        mxv = -999999
        for act in legal :
            succ_state = gameState.generateSuccessor(0 ,act)
            #px , py = succ_state.getPacmanPosition()
            #walls = succ_state.getWalls()
            v= self.value(succ_state , 0 , 'min')
            if v>= mxv :#and not act == 'Stop' and not walls[px][py]:
                mxv =v
                ans_act = act        
        #print (ans_act)
        return ans_act
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def value(self , gameState , cur_depth  , alpha = -9999999990 , beta=9999990 , agent=1  ):
        #print( cur_depth , alpha , beta, agent , gameState.isWin() or gameState.isLose())
        if cur_depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0 :
            return self.maxVal(gameState , cur_depth ,alpha , beta)
        else :
            return self.minVal(gameState ,cur_depth  , alpha,beta , agent )
    def maxVal(self , gameState , d , alpha , beta ):
        v= -99999999
        legalActs = gameState.getLegalActions(0)
        for act in legalActs :
            succ_state= gameState.generateSuccessor(0 , act)
            v= max(v , self.value(succ_state , d, alpha , beta , 1 ))
            if v> beta :
                return v 
            alpha = max(v, alpha)
            # print("alpha =" , alpha)
            # print("beta =" , beta)
        return v
    def minVal(self , gameState , d , alpha , beta , agent):
        #print ("min")
        v= 9999999999
        legalActs = gameState.getLegalActions(agent)
        for act in legalActs :
            succ_state = gameState.generateSuccessor(agent , act)
            if agent+1 == gameState.getNumAgents() :
                v = min (v , self.value(succ_state , d+1 , alpha , beta , 0))
            else :
                v= min (v , self.value(succ_state , d , alpha , beta , agent+1))
                #print (v , alpha)
            if v < alpha :
                return v
            beta = min (beta , v)
        return v
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #print (gameState.getNumAgents())
        legals = gameState.getLegalActions(0)
        mxv =-99999999
        alpha_root =-99999999
        ans_action =None
        for act in legals:
            succ_state = gameState.generateSuccessor(0 , act)
            v= self.value(succ_state , 0 , alpha= alpha_root)
            if v>mxv :
                mxv=v
                ans_action = act
                alpha_root = v
        return ans_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def value(self , gameState , cur_depth , agent=1):
        #print(cur_depth)
        if self.depth == cur_depth or gameState.isWin() or gameState.isLose():
            #print("yes !")
            return self.evaluationFunction(gameState)
        if agent == 0 :
            return self.MaxVal(gameState , cur_depth )
        else :
            return self.ExpecVal(gameState , cur_depth , agent)
    def MaxVal(self , gameState , d):
        v= -99999999
        legalActs = gameState.getLegalActions(0)
        for act in legalActs :
            succ_state = gameState.generateSuccessor(0 , act)
            v= max(v, self.value(succ_state , d , 1))
        return v
    def ExpecVal(self , gameState , d , agent ):
        v=0
        legalActs = gameState.getLegalActions(agent)
        for act in legalActs :
            succ_state = gameState.generateSuccessor(agent , act)
            if agent +1 == gameState.getNumAgents():
                v+=self.value(succ_state , d+1 , 0)
            else :
                v+= self.value(succ_state , d, agent+1)
        return v/ len(legalActs)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        mxv=-999999
        rightAction=None
        legalActs = gameState.getLegalActions(0)
        for act in legalActs :
            if not act == 'Stop':
                succ_state=gameState.generateSuccessor(0 ,act)
                v= self.value(succ_state , 0 , 1)
                if v> mxv  :
                    mxv=v
                    rightAction= act
        #print(rightAction)        
        return rightAction
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    global zipy
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    win =0
    lose =0
    if currentGameState.isWin():
        win = 10000000000000000000000000000
    elif currentGameState.isLose():
        lose = -10000000000000000000000000000
    curPos = currentGameState.getPacmanPosition()
    curGhostsPos = [ghostState.start.pos for ghostState in currentGameState.getGhostStates()]
    curNearstGhost = min ([euclideanDistance(curPos, Gpos) for Gpos in curGhostsPos ])
    curFood = currentGameState.getFood()
    curFoodList = curFood.asList()
    curFoodDis= [euclideanDistance(curPos , z) for z in curFoodList]
    nearstFood =min(curFoodDis)
    curCaps = currentGameState.getCapsules()
    curCapsDis = [euclideanDistance(curPos , z) for z in curCaps]
    avg_dis_caps = sum(curCapsDis)/len(curCapsDis)
    nearstCap = min(curCapsDis)
    average_distance_to_food= sum(curFoodDis)/len(curFoodDis)
    total_eval= win+ lose+nearstFood+2*nearstCap + 4*average_distance_to_food+7*avg_dis_caps\
         - 7*curNearstGhost + currentGameState.getScore() 
         # I have choosed these numbers randomly but they can be considered as weights for each parameter
    # this evaluation function is bullshit Agent will play for a very long time without even losing or wining 
    # but there is a good one posted on github: (https://raw.githubusercontent.com/JoshGelua/UC-Berkeley-Pacman-Project2/master/multiAgents.py)
    #print(total_eval)
    return (total_eval)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
