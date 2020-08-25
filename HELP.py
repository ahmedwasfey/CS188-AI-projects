    # food_grid = self.getFood(gameState)
    # food_list = food_grid.asList()
    # ans_act =[] 
    # min_dis = 9999999
    # for act in actions :
    #   if not act =='Stop':
    #     successor = gameState.generateSuccessor(self.index, act)
    #     myPos = successor.getAgentState(self.index).getPosition()
    #     dis = min([ self.distancer.getDistance(myPos, x) for x in food_list ])
    #     if dis <= min_dis :
    #        dis = min_dis
    #        ans_act.append(act )

    # #print(ans_act)
    # return  random.choice(ans_act)
    # return random.choice(actions)

    # You can profile your evaluation time by uncommenting these lines