# searchAgents.py
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


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActionSequence(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, child
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def expand(self, state):
        """
        Returns child states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (child, action, stepCost), where 'child' is a
         child to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that child
        """

        children = []
        for action in self.getActions(state):
            nextState = self.getNextState(state, action)
            cost = self.getActionCost(state, action, nextState)
            children.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return children

    def getActions(self, state):
        possible_directions = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        valid_actions_from_state = []
        for action in possible_directions:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                valid_actions_from_state.append(action)
        return valid_actions_from_state

    def getActionCost(self, state, action, next_state):
        assert next_state == self.getNextState(state, action), (
            "Invalid next state passed to getActionCost().")
        return self.costFn(next_state)

    def getNextState(self, state, action):
        assert action in self.getActions(state), (
            "Invalid action passed to getActionCost().")
        x, y = state
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        return (nextx, nexty)

    def getCostOfActionSequence(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

# Questao 4 - CornersProblem

class CornersProblem(search.SearchProblem):  #! QUESTAO 4

    def __init__(self, startingGameState):
        """
        Inicializa o problema:
        - Armazena as paredes do labirinto
        - Define posição inicial do Pacman
        - Define os cantos do labirinto
        """
        self.walls = startingGameState.getWalls()  # Matriz de paredes
        self.startingPosition = startingGameState.getPacmanPosition()  # Posição inicial do Pacman

        # Define os cantos (inferior esquerdo, superior esquerdo, inferior direito, superior direito)
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))

        # Alerta caso algum canto não tenha comida (opcional)
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))

        self._expanded = 0  # Contador de nós expandidos
        self.startingGameState = startingGameState  # Guardamos referência do estado do jogo

    def getStartState(self):
        """
        Retorna o estado inicial do problema.
        Aqui, o estado é uma tupla:
        (posição atual do Pacman, cantos visitados)
        """
        return (self.startingPosition, ())  # Nenhum canto visitado no início

    def isGoalState(self, state):
        """
        Retorna True se todos os quatro cantos já foram visitados.
        """
        _, visitedCorners = state
        return len(visitedCorners) == 4

    def expand(self, state):
        """
        Gera todos os filhos do estado atual:
        - Para cada ação possível, calcula a próxima posição
        - Atualiza cantos visitados
        - Retorna lista de tuplas (nextState, action, cost)
        """
        children = []
        currentPosition, visitedCorners = state

        for action in self.getActions(state):  # Pega todas ações válidas
            nextPosition = self.getNextPosition(currentPosition, action)  # Próxima posição do Pacman

            # Se for um canto ainda não visitado, adiciona aos visitados
            if nextPosition in self.corners and nextPosition not in visitedCorners:
                newVisited = visitedCorners + (nextPosition,)
            else:
                newVisited = visitedCorners

            # Garantir que os cantos visitados sejam únicos e ordenados
            newVisited = tuple(sorted(set(newVisited)))
            nextState = (nextPosition, newVisited)  # Próximo estado completo
            children.append((nextState, action, 1))  # Adiciona à lista de filhos (custo = 1)

        self._expanded += 1  # Incrementa contador de nós expandidos
        return children

    def getActions(self, state):
        """
        Retorna todas ações possíveis a partir do estado atual, 
        considerando as paredes.
        """
        possible_directions = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        valid_actions_from_state = []

        x, y = state[0]  # Posição atual
        for action in possible_directions:
            dx, dy = Actions.directionToVector(action)  # Converte direção em vetor (dx, dy)
            nextx, nexty = int(x + dx), int(y + dy)

            if not self.walls[nextx][nexty]:  # Checa se não bate na parede
                valid_actions_from_state.append(action)  # Ação válida

        return valid_actions_from_state

    def getActionCost(self, state, action, next_state):
        """
        Retorna o custo da ação. Aqui, todas as ações têm custo 1.
        """
        assert next_state == self.getNextState(state, action), (
            "Invalid next state passed to getActionCost().")
        return 1
    
    def getNextPosition(self, position, action):
        """
        Calcula a próxima posição do Pacman a partir da posição atual e da ação.
        Não altera os cantos visitados.
        """
        x, y = position
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        return (nextx, nexty)

    def getNextState(self, state, action):
        """
        Calcula o próximo estado completo:
        - Nova posição do Pacman
        - Atualiza cantos visitados caso chegue em um canto
        """
        currentPosition, visitedCorners = state
        nextPosition = self.getNextPosition(currentPosition, action)

        # Adiciona canto visitado, se ainda não estiver na lista
        if nextPosition in self.corners and nextPosition not in visitedCorners:
            newVisited = visitedCorners + (nextPosition,)
        else:
            newVisited = visitedCorners

        # Mantém os cantos visitados únicos e ordenados
        newVisited = tuple(sorted(set(newVisited)))
        return (nextPosition, newVisited)

    def getCostOfActionSequence(self, actions):
        """
        Calcula o custo total de uma sequência de ações.
        Se alguma ação for ilegal (bate na parede), retorna um valor grande.
        """
        if actions == None: return 999999
        x, y = self.startingPosition

        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999  # Movimento ilegal

        return len(actions)  # Custo = número de passos

# Questao 5 - Heurística para CornersProblem 
def cornersHeuristic(state, problem):  #! QUESTAO 5
    """
    Heurística para o CornersProblem.
    Estima o menor custo restante para visitar todos os cantos ainda não visitados.
    Considerando apenas a distância até o canto mais distante não visitado.
    """

    from util import manhattanDistance  # distância de Manhattan

    # position é a posição atual do Pacman (x, y)
    # visitedCorners é a tupla com os cantos já visitados
    position, visitedCorners = state

    # cria uma lista com os cantos que ainda não foram visitados
    unvisited = [corner for corner in problem.corners if corner not in visitedCorners]

    # se todos os cantos já foram visitados, não há custo restante
    if not unvisited:
        return 0

    # distância de Manhattan de posição atual até cada canto não visitado
    # e retorna a maior dessas distâncias
    # estimativa do custo restante para visitar todos os cantos
    return max(manhattanDistance(position, corner) for corner in unvisited)



class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def expand(self, state):
        "Returns child states, the actions they require, and a cost of 1."
        children = []
        self._expanded += 1 # DO NOT CHANGE
        for action in self.getActions(state):
            next_state = self.getNextState(state, action)
            action_cost = self.getActionCost(state, action, next_state)
            children.append( ( next_state, action, action_cost) )
        return children

    def getActions(self, state):
        possible_directions = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        valid_actions_from_state = []
        for action in possible_directions:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                valid_actions_from_state.append(action)
        return valid_actions_from_state

    def getActionCost(self, state, action, next_state):
        assert next_state == self.getNextState(state, action), (
            "Invalid next state passed to getActionCost().")
        return 1

    def getNextState(self, state, action):
        assert action in self.getActions(state), (
            "Invalid action passed to getActionCost().")
        x, y = state[0]
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        nextFood = state[1].copy()
        nextFood[nextx][nexty] = False
        return ((nextx, nexty), nextFood)

    def getCostOfActionSequence(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem
    
# Questao 6 - Heurística para FoodSearchProblem
def foodHeuristic(state, problem): 
    """
    Heurística para o FoodSearchProblem.
    Essa solução é mais demorada pois o mazeDistance roda um BFS para cada comida.
    """

    position, foodGrid = state

    # lista de coordenadas da comida que ainda não foi comida
    foodList = foodGrid.asList()

    # se não há comida restante, custo é zero (estado objetivo)
    if not foodList:
        return 0

    # calcula a maior distância real (mazeDistance) entre a posição atual e qualquer comida
    # isso é melhor que Manhattan simples, porque leva em conta paredes do labirinto
    maxDistance = 0
    for food in foodList:
        dist = mazeDistance(position, food, problem.startingGameState)
        if dist > maxDistance:
            maxDistance = dist

    return maxDistance

# Questo 7 - Busca subótima
class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateChild(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState):
        """
        Retorna um caminho (lista de ações) até a comida mais próxima,
        começando a partir de gameState.
        """
        problem = AnyFoodSearchProblem(gameState)

        from search import breadthFirstSearch
        return breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    Problema de busca para encontrar um caminho até qualquer comida.
    """
    def __init__(self, gameState):
        # Guarda a grade de comida para referência
        self.food = gameState.getFood()

        # Configurações herdadas do PositionSearchProblem
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # NÃO ALTERAR

    def isGoalState(self, state):
        """
        Um estado é objetivo se a posição atual contém comida.
        """
        x, y = state
        return self.food[x][y]  # True se houver comida nessa posição

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
