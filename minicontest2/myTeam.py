# myTeam.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """  

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''
    self.depth= 2
    self.opId=None
    self.myId = None
    self.start = gameState.getAgentState(self.index).getPosition()
  def evaluation(self , gameState):
    op = self.getOpponents(gameState)
    myPos= gameState.getAgentState(self.index).getPosition()
    myTeam = self.getTeam(gameState)
    teamPos = [gameState.getAgentState(x).getPosition() for x in myTeam]
    opponentState = [gameState.getAgentState(x) for x in op]
    opponentsPos = [x.getPosition() for x in opponentState]
    opponentsDis = [self.distancer.getDistance(myPos , z) for z in opponentsPos]
    teamDis = [self.distancer.getDistance(myPos , z) for z in teamPos]
    if self.index == self.myId:
        x=3000* self.getScore(gameState)
        return (min(opponentsDis))+3*max(teamDis)
    else :
      return  (min(opponentsDis))

  def value (self , gameState ,my_depth , agent  ):
      #print(my_depth) 
      if my_depth >= self.depth :
          #print (self.getScore(gameState) , "--------------------------------------")
          return self.evaluation(gameState)
          
      if  agent== self.opId:
          return  self.minv(gameState, my_depth )
      elif agent ==self.myId :
          return self.maxv(gameState , my_depth )
  def maxv (self , gameState,d ):
      
      v= -9999999999
      ans = None
      leg_act = gameState.getLegalActions(self.myId)
      #leg_act.remove('Stop')
      for act in leg_act :
          sucss_state = gameState.generateSuccessor(self.myId , act)
          v =max(v, self.value(sucss_state,d,self.opId )) 
      return v 
  def minv(self , gameState, d   ):
      v = 99999999999
      ans =None       
      leg_act = gameState.getLegalActions(self.opId)
      for act in leg_act :
          sucss_state = gameState.generateSuccessor(self.opId , act)
          v =min (v, self.value(sucss_state , d+1, self.myId ))    
      return v
  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    
    actions = gameState.getLegalActions(self.index)
    opponents = self.getOpponents(gameState)
    opponentsPos = [gameState.getAgentState(x).getPosition() for x in opponents ]
    myPos = gameState.getAgentState(self.index).getPosition()
    opponentsDis = [self.distancer.getDistance(myPos, x)  for x in opponentsPos]
    for i in range(len(opponentsDis)):
      if opponentsDis[i]<13 :
        
        if gameState.getAgentState(opponents[i]).isPacman :
        
          self.myId = opponents[i]
          self.opId = self.index  
          bestAction =None
          mnVal = 99999999
          for act in actions :
            successorState = gameState.generateSuccessor(self.index , act)
            val = self.value(successorState , 0 , self.opId )
            if val < mnVal:
              mnVal = val 
              bestAction = act 
          return bestAction



        elif opponentsDis[i]<8:
          self.myId = self.index
          self.opId = opponents[i]
          bestAction =None
          maxVal = -99999999
          for act in actions :
            successorState = gameState.generateSuccessor(self.index , act)
            val = self.value(successorState , 0 , self.opId )
            if val > maxVal:
              maxVal = val 
              bestAction = act 
          return bestAction







    #start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    #print ('eval time for agent %d: %.4f' % (self.index, time.time() - start))

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      #print ("hi")
      for action in actions:
        successor =gameState.generateSuccessor(self.index, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)



  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    #print(features , weights)
    return features * weights

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = gameState.generateSuccessor(self.index , action)
    foodList = self.getFood(successor).asList()    
    features['successorScore'] = -len(foodList)#self.getScore(successor)

    # Compute distance to the nearest food

    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}
