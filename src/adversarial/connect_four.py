import numpy as np

ROWS, COLS = 6, 7

class ConnectFour:
    '''
    Connect Four game class
    This class represents the game board and provides methods to play the game.
    It includes methods to check for available moves, make moves, check for a winner, etc.
    '''

    def __init__(self, board=None, current='X'):
        ''' Initialize the game board and current player
        :param board: 2D array representing the game board
        :param current: Current player ('X' or 'O')
        '''
        self.board = board.copy() if board is not None else np.full((ROWS, COLS), ' ')
        self.current = current

    def available_moves(self):
        ''' Get a list of available moves (columns) where the top row is empty
        :return: List of available columns
        '''
        # Check the top row of each column for available moves
        # If the top row is empty, the column is available
        return [c for c in range(COLS) if self.board[0][c] == ' ']

    def make_move(self, col):
        ''' Make a move in the specified column
        :param col: Column index to make the move
        :return: True if the move was successful, False if the column is full
        '''
        # Iterate from the bottom row to the top row
        # Find the first empty cell in the specified column
        # Place the current player's symbol in that cell
        # Switch to the other player
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current
                self.current = 'O' if self.current == 'X' else 'X'
                return True
        return False

    def copy(self):
        ''' Create a copy of the current game state
        :return: A new ConnectFour object with the same board and current player
        '''
        # Create a new ConnectFour object with a copy of the current board
        # and the same current player
        # This is useful for simulating moves without modifying the original game state when using MCTS or other algorithms.
        return ConnectFour(self.board.copy(), self.current)

    def winner(self):
        ''' Check for a winner in the game
        :return: 'X' if player X wins, 'O' if player O wins, None if no winner
        '''
        for r in range(ROWS):
            for c in range(COLS - 3):
                line = self.board[r, c:c + 4]
                if np.all(line == line[0]) and line[0] != ' ':
                    return line[0]
        for r in range(ROWS - 3):
            for c in range(COLS):
                line = self.board[r:r + 4, c]
                if np.all(line == line[0]) and line[0] != ' ':
                    return line[0]
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                line = [self.board[r + i][c + i] for i in range(4)]
                if all(x == line[0] and x != ' ' for x in line):
                    return line[0]
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                line = [self.board[r - i][c + i] for i in range(4)]
                if all(x == line[0] and x != ' ' for x in line):
                    return line[0]
        return None

    def full(self):
        ''' Check if the board is full (no available moves)
        :return: True if the board is full, False otherwise
        '''
        # Check if the top row of each column is not empty
        return all(self.board[0][c] != ' ' for c in range(COLS))

    def game_over(self):
        ''' Check if the game is over (either a win or a draw)
        :return: True if the game is over, False otherwise
        '''
        # Check if there is a winner or if the board is full
        return self.winner() or self.full()