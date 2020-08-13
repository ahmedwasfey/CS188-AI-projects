# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time , random
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
my_dic ={} 
taken ={}
steps={}
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        food = state.getFood()
        if len(my_dic)==0:
            food_pos = food.asList()
            walls = state.getWalls()
            top =walls.height-1
            right = walls.width-1
            
            for i in range(1,right):
                for j in range(1, top):
                    #print (i,j) 
                    if not walls[i][j]:
                        my_dic[(i,j)]=[]
                        for k in food_pos :
                            dis=util.manhattanDistance((i,j), k)
                            #dis=util.euclideanDistance((i,j), k)
                            #dis= mazeDistance((i,j), k ,state)
                            my_dic[(i,j)].append([dis , k])
                        my_dic[(i,j)].sort()
                        #my_dic[(i,j)].reverse()
                        # print i , j ,  my_dic[(i,j)]
        position = state.getPacmanPosition(self.index)
        #print (taken)
        if self.index in taken.keys():
            fx,fy = taken[self.index]
            if food[fx][fy]:
               turn , path = steps[self.index]
               steps[self.index][0]=turn+1
               #print (path[turn])
               return path[turn]
        for i in my_dic[position]:
            fx,fy = i[1]
            if food[fx][fy]:
              if i[1] not in taken.values():  
                taken[self.index]=i[1]
                prob = PositionSearchProblem(state, start= position , goal=i[1],warn=False, visualize=False)
                steps[self.index]=[1,search.bfs(prob)] 
                return steps[self.index][1][0]
        ff= food.asList()
        prob = PositionSearchProblem(state, start= position , goal=ff[0],warn=False, visualize=False)
        steps[self.index]=[1,search.bfs(prob)] 
        return steps[self.index][1][0]
        ########## old trivial failed solution #####
               
        #         indx = self.index
        #         if  indx in my_dic.keys():
        #             turn , path = my_dic[indx]
        #             if turn <len(path):
        #                 my_dic[indx][0]= turn+1
        #                 return path[turn]         
        #             print("found" , px.getStartState())
        #         food = state.getFood()
        #         food_list = food.asList()
        #         r = random.randrange(len(food_list))
        #         dot = food_list[r-1]
        #         print (food[dot[0]][dot[1]])
        #         startingPosition = state.getPacmanPosition(indx)
        #         print (startingPosition, dot)
        #         prob = PositionSearchProblem(state,agentIndex= indx ,start=startingPosition ,goal= dot )
        #         print ( prob.getStartState())
        #         my_dic[indx]=[1,search.bfs(prob)]
        #         return my_dic[indx][1][0]
        
        raise NotImplementedError()

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
       # self.walls = s
        #self.top, self.right = self.walls.height-1, self.walls.width-1
        return 0
        "*** YOUR CODE HERE" 

        raise NotImplementedError()

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)
        return search.bfs(problem)
        
        util.raiseNotDefined()

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        return self.food[x][y]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
