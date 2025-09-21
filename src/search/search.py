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
from util import Queue


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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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


# Questao 1 - DFS
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
     # Pilha para DFS
    frontier = util.Stack()
    # Cada nó = (estado, caminho até aqui)
    frontier.push((problem.getStartState(), []))
    visited = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if state in visited:
            continue
        visited.add(state)

        # Objetivo alcançado
        if problem.isGoalState(state):
            return path

        # Expansão do nó
        for successor, action, _ in problem.expand(state):
            if successor not in visited:
                new_path = path + [action]
                frontier.push((successor, new_path))

    # Caso não encontre solução
    return []

# Questao 2 - BFS
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    # Fila para controlar a fronteira
    frontier = Queue()
    frontier.push((problem.getStartState(), []))
    
    # Conjunto de estados visitados
    visited = set()
    
    while not frontier.isEmpty():
        state, path = frontier.pop()
        
        # Verifica se é objetivo
        if problem.isGoalState(state):
            return path
        
        if state not in visited:
            visited.add(state)
            
            # Expande sucessores
            for successor, action, _ in problem.expand(state):
                if successor not in visited:
                    frontier.push((successor, path + [action]))
    
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Questao 3 - A*
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Fila de prioridade para A*
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()
    # Cada nó = (estado, caminho até aqui, custo acumulado)
    frontier.push((start_state, [], 0), heuristic(start_state, problem))
    visited = dict()  # estado: menor custo encontrado

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        # Se já visitou com custo menor, ignora
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        # Objetivo alcançado
        if problem.isGoalState(state):
            return path

        # Expansão do nó
        for successor, action, step_cost in problem.expand(state):
            new_cost = cost + step_cost
            if successor not in visited or visited[successor] > new_cost:
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, path + [action], new_cost), priority)

    # Caso não encontre solução
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
