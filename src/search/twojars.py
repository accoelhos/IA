import search
import random
from random import randint
import util

# Module Classes

class TwoJarsState:
    """
    Representa um estado dos dois jarros.
    """

    def __init__(self, volumes):
        self.jars = {"J4": volumes[0], "J3": volumes[1]}
        assert 0 <= self.jars["J4"] <= 4
        assert 0 <= self.jars["J3"] <= 3

    def isGoal(self):
        """
        Retorna True se o jarro de 4 litros tem 2 litros.
        """
        return self.jars["J4"] == 2

    def legalMoves(self):
        """
        Retorna a lista de movimentos válidos a partir do estado atual.
        """
        moves = []
        J4, J3 = self.jars["J4"], self.jars["J3"]
        
        # Encher jarros
        if J4 < 4: moves.append("fillJ4")
        if J3 < 3: moves.append("fillJ3")
        
        # Esvaziar jarros
        if J4 > 0: moves.append("emptyJ4")
        if J3 > 0: moves.append("emptyJ3")
        
        # Despejar de um jarro no outro
        if J3 > 0 and J4 < 4: moves.append("pourJ3intoJ4")
        if J4 > 0 and J3 < 3: moves.append("pourJ4intoJ3")
        
        return moves

    def result(self, move):
        """
        Retorna um novo estado resultante de aplicar o movimento.
        """
        J4, J3 = self.jars["J4"], self.jars["J3"]
        newJ4, newJ3 = J4, J3

        if move == "fillJ4":
            newJ4 = 4
        elif move == "fillJ3":
            newJ3 = 3
        elif move == "emptyJ4":
            newJ4 = 0
        elif move == "emptyJ3":
            newJ3 = 0
        elif move == "pourJ3intoJ4":
            transfer = min(J3, 4 - J4)
            newJ3 -= transfer
            newJ4 += transfer
        elif move == "pourJ4intoJ3":
            transfer = min(J4, 3 - J3)
            newJ4 -= transfer
            newJ3 += transfer
        else:
            raise Exception(f"Movimento inválido: {move}")

        return TwoJarsState((newJ4, newJ3))

    def __eq__(self, other):
        return isinstance(other, TwoJarsState) and self.jars == other.jars

    def __hash__(self):
        return hash((self.jars["J4"], self.jars["J3"]))

    def __getAsciiString(self):
        return f"[J4: {self.jars['J4']}/4 | J3: {self.jars['J3']}/3]"

    def __str__(self):
        return self.__getAsciiString()


class TwoJarsSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the Two Jars domain

      Each state is represented by an instance of an TwoJarsState.
    """
    def __init__(self, start_state):
        "Creates a new TwoJarsSearchProblem which stores search information."
        self.start_state = start_state

    def getStartState(self):
        return self.start_state

    def isGoalState(self,state):
        return state.isGoal()

    def expand(self,state):
        """
          Returns list of (child, action, stepCost) pairs where
          each child is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        child = []
        for a in self.getActions(state):
            next_state = self.getNextState(state, a)
            child.append((next_state, a, self.getActionCost(state, a, next_state)))
        return child

    def getActions(self, state):
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        assert next_state == state.result(action), (
            "getActionCost() called on incorrect next state.")
        return 1

    def getNextState(self, state, action):
        assert action in state.legalMoves(), (
            "getNextState() called on incorrect action")
        return state.result(action)

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def createRandomTwoJarsState(moves=10):
    """
      moves: number of random moves to apply

      Creates a random state by applying a series 
      of 'moves' random moves to a solved state.
    """
    volume_of_J3 = randint(0, 3)
    a_state = TwoJarsState((2,volume_of_J3))
    for i in range(moves):
        # Execute a random legal move
        a_state = a_state.result(random.sample(a_state.legalMoves(), 1)[0])
    return a_state

if __name__ == '__main__':
    start_state = createRandomTwoJarsState(8)
    print('A random initial state:')
    print(start_state)

    problem = TwoJarsSearchProblem(start_state)
    path = search.breadthFirstSearch(problem)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = start_state
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1
