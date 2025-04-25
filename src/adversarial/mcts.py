import numpy as np
import math
import random

class MCTSNode:
    '''
    Monte Carlo Tree Search Node
    This class represents a node in the Monte Carlo Tree Search (MCTS) algorithm.
    It includes methods for selection, expansion, simulation, and backpropagation.
    '''

    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.available_moves()

    def ucb1(self, c=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)

    def select_child(self):
        return max(self.children, key=lambda child: child.ucb1())

    def expand(self):
        move = self.untried_moves.pop()
        new_game = self.game.copy()
        new_game.make_move(move)
        child = MCTSNode(new_game, parent=self, move=move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result


def mcts(root_game, iterations=200):
    '''
    Monte Carlo Tree Search algorithm
    :param root_game: The initial game state
    :param iterations: Number of iterations to run the MCTS
    :return: The best move found by MCTS
    '''

    root = MCTSNode(root_game)

    for _ in range(iterations):
        node = root
        game = root_game.copy()

        # Selection
        while node.untried_moves == [] and node.children:
            node = node.select_child()
            game.make_move(node.move)

        # Expansion
        if node.untried_moves:
            node = node.expand()
            game = node.game.copy()

        # Simulation
        while not game.game_over():
            game.make_move(random.choice(game.available_moves()))

        winner = game.winner()
        if winner == 'X':
            result = 1
        elif winner == 'O':
            result = -1
        else:
            result = 0

        # Backpropagation
        while node is not None:
            perspective = 1 if node.game.current == 'O' else -1
            node.update(perspective * result)
            node = node.parent

    return max(root.children, key=lambda c: c.visits).move

