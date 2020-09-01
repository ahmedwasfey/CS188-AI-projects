# valueIterationAgents.py
# ----------------------- 
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.actions= util.Counter()
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        # states= self.mdp.getStates()
        # print( self.mdp.getStates())
        # actions =  self.mdp.getPossibleActions(states[1])
        # print(actions)
        # print(self.mdp.getTransitionStatesAndProbs(states[1], actions[0]))
        #print(self.mdp.getReward(states[0], action[0], nextState))
        #print(self.mdp.isTerminal(state))

        states= self.mdp.getStates()
        for iteration in range(self.iterations): 
            vOld = util.Counter()
            for state in states:
                mxval = -9999999
                actions = self.mdp.getPossibleActions(state)
                for act in actions :
                    #sPrimes= self.mdp.getTransitionStatesAndProbs(state, act)
                    val =self.getQValue(state , act)
                    if val > mxval:
                        mxval= val 
                        vOld[state]=val
                        #self.actions[state]             
            #print(vOld)
            self.values= vOld
            

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        sprimes = self.mdp.getTransitionStatesAndProbs(state, action)
        val =0
        for (sprime , prob) in sprimes:
            val+= prob*(self.mdp.getReward(state , action , sprime)+ self.discount* self.values[sprime])
        return val
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #return self.actions[state]
        actions =  self.mdp.getPossibleActions(state)
        if len(actions)==0 :
            return None 
        else :
            ans_act =None 
            mxq = -999999999999
            for act in actions :
                qval = self.getQValue(state , act)
                if qval> mxq:
                    mxq =qval
                    ans_act=act
            #print(ans_act)
            return ans_act
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        idx =0 
        states = self.mdp.getStates()
        for iteration in range(self.iterations) :
            next_value=-9999999
            state = states[idx%(len(states))]
            actions = self.mdp.getPossibleActions(state)
            for act in actions :
                val = self.getQValue(state , act)
                next_value = max(val , next_value)
            if len(actions)>0 :
                self.values[state]= next_value
            idx+=1

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        terminals= []
        predecessors ={}
        states = self.mdp.getStates()
        for state in states :
            #if self.mdp.isTerminal(state): terminals.append(state)
            actions = self.mdp.getPossibleActions(state)
            for action in actions :
                sprimes =[x[0] for x in self.mdp.getTransitionStatesAndProbs(state , action)]
                for sprime in sprimes :
                    if not sprime in predecessors : predecessors[sprime]= set()
                    predecessors[sprime].add(state)   
        pq = util.PriorityQueue()
        for state in states:
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                mxq = -9999999
                for action in actions :
                    qval = self.getQValue(state , action)
                    mxq = max(qval , mxq)
                pq.update(state , - abs(self.values[state] - mxq))
        for iteration in range(self.iterations):
            if pq.isEmpty(): return 
            state = pq.pop()
            actions = self.mdp.getPossibleActions(state)
            self.values[state]=max([self.getQValue( state , act) for act in actions])
            for p in predecessors[state]:
                mxq = -999999
                for act in self.mdp.getPossibleActions(p):
                    mxq = max (self.getQValue(p , act) , mxq)
                diff = abs(self.values[p]-mxq)
                if diff > self.theta :
                    pq.update(p , - diff)
        print(pq.heap)
        print(predecessors)

