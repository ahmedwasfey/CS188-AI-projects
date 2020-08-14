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
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    print problem 
    """

    st= util.Stack()
    visited = set()
    start_node=(problem.getStartState(), [])
    st.push(start_node)

    while not st.isEmpty():
        (cur_state , cur_path) = st.pop()
        #print cur_path
        if problem.isGoalState(cur_state):
           return cur_path
        if cur_state not in visited :
            visited.add(cur_state)
            for child , action , cost in problem.getSuccessors(cur_state):
                child_node=(child, cur_path+[action])
                st.push(child_node)
               
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"  
    # print type(problem.getStartState())
    # print (problem.getStartState())
    # print problem.getSuccessors(problem.getStartState())
    q= util.Queue()
    visited =[]
    start_node=(problem.getStartState(), [])
    q.push(start_node)
    while not q.isEmpty():
        cur_state , cur_path = q.pop()
        #print cur_path
        if problem.isGoalState(cur_state):
            #print cur_state
            return cur_path
        if not cur_state in visited :
            visited.append(cur_state)
            for child , action , cost in problem.getSuccessors(cur_state):
                child_node=(child, cur_path+[action])
                #print child
                q.push(child_node)
               
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
 
    q= util.PriorityQueue()
    visited = []
    start_node=(problem.getStartState() , [] , 0)
    q.update(start_node,0)
    while not q.isEmpty():
        cur_state , cur_path , cur_cost = q.pop()
        #print cur_path
        if problem.isGoalState(cur_state):
           return cur_path
        if not cur_state in visited :
            visited.append(cur_state)
            for child , action , cost in problem.getSuccessors(cur_state):
                child_cost = cur_cost + cost 
                child_node=(child, cur_path+[action] , child_cost)   
                q.update(child_node, child_cost)
            
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    start_node = (problem.getStartState(), [] , 0)
    q= util.PriorityQueue()
    q.update(start_node,0)
    while not q.isEmpty():
        (cur_state, cur_path , cur_cost)= q.pop()
        if problem.isGoalState(cur_state):
            return cur_path
        if cur_state not in visited :
            visited.append(cur_state)
            for child , action , cost in problem.getSuccessors(cur_state):
                new_cost = cur_cost+cost 
                h= new_cost+heuristic(child, problem)
                child_node =(child , cur_path+[action], new_cost)
                q.update(child_node, h)



    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
