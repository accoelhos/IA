import search
import random
from random import randint
import util

# Module Classes

# implementada
class TwoJarsState:
    """
    Representa um estado dos dois jarros.
    """
    def __init__(self, volumes):
        # dicionario para armazenar volume atual de cada jarro
        self.jars = {"J4": volumes[0], "J3": volumes[1]}
        # garante que os volumes nao ultrapassem as capacidades dos jarros
        assert 0 <= self.jars["J4"] <= 4
        assert 0 <= self.jars["J3"] <= 3

    def isGoal(self):
        # verifica se o jarro de 4 litros contem exatamente 2 litros
        return self.jars["J4"] == 2

    def legalMoves(self):
        # retorna a lista de movimentos validos a partir do estado atual
        moves = []
        J4, J3 = self.jars["J4"], self.jars["J3"]
        
        # encher jarros
        if J4 < 4: moves.append("fillJ4")
        if J3 < 3: moves.append("fillJ3")
        
        # esvaziar jarros
        if J4 > 0: moves.append("emptyJ4")
        if J3 > 0: moves.append("emptyJ3")
        
        # transferir agua de um jarro para o outro
        if J3 > 0 and J4 < 4: moves.append("pourJ3intoJ4")
        if J4 > 0 and J3 < 3: moves.append("pourJ4intoJ3")
        
        return moves

    def result(self, move):
        # retorna um novo estado resultante da aplicacao do movimento
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
            raise Exception(f"movimento invalido: {move}")

        return TwoJarsState((newJ4, newJ3))

    def __eq__(self, other):
        return isinstance(other, TwoJarsState) and self.jars == other.jars

    def __hash__(self):
        return hash((self.jars["J4"], self.jars["J3"]))

    def __getAsciiString(self):
        return f"[J4: {self.jars['J4']}/4 | J3: {self.jars['J3']}/3]"

    def __str__(self):
        return self.__getAsciiString()


# classe que define o problema de busca dos dois jarros
class TwoJarsSearchProblem(search.SearchProblem):
    """
    implementacao de um problema de busca para o dominio dos dois jarros
    cada estado e representado por uma instancia de TwoJarsState
    """
    def __init__(self, start_state):
        # define o estado inicial do problema
        self.start_state = start_state

    def getStartState(self):
        # retorna o estado inicial
        return self.start_state

    def isGoalState(self, state):
        # verifica se o estado atual e um estado objetivo
        return state.isGoal()

    def expand(self, state):
        # retorna lista de tuplas (estado_filho, acao, custo) para cada sucessor
        child = []
        for a in self.getActions(state):
            next_state = self.getNextState(state, a)
            child.append((next_state, a, self.getActionCost(state, a, next_state)))
        return child

    def getActions(self, state):
        # retorna as acoes validas a partir do estado atual
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        # retorna o custo de executar uma acao (neste caso, sempre 1)
        assert next_state == state.result(action), (
            "getActionCost() chamado em estado incorreto")
        return 1

    def getNextState(self, state, action):
        # retorna o proximo estado apos executar a acao
        assert action in state.legalMoves(), (
            "getNextState() chamado em acao incorreta")
        return state.result(action)

    def getCostOfActionSequence(self, actions):
        # retorna o custo total de uma sequencia de acoes
        return len(actions)


def createRandomTwoJarsState(moves=10):
    # cria um estado aleatorio aplicando 'moves' movimentos aleatorios a partir do estado objetivo
    volume_of_J3 = randint(0, 3)
    a_state = TwoJarsState((2, volume_of_J3))
    for i in range(moves):
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

        input("Press return for the next state...")
        i += 1