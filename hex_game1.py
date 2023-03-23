# Created by Luke Schultz
# Winter 2023
#
# 1d numpy array board representation.
# Board Representation:
# 3 1 1 1 3    3 1 1 1 3
# 2 0 0 0 2     2 0 0 0 2
# 2 0 0 0 2 ->   2 0 0 0 2
# 2 0 0 0 2       2 0 0 0 2
# 3 1 1 1 3        3 1 1 1 3
# Where BORDER = 3, BLACK = 1, WHITE = 2, BLANK = 0


from copy import deepcopy
import numpy as np


# board constant
BLANK = 0
BLACK = 1
WHITE = 2
BORDER = 3


class Hex1:
    def __init__(self, game_dim: int):
        self.game_dim = game_dim  # Side length of the game
        self.board_dim = self.game_dim + 2  # Side length of the array repr
        self.board_size = self.board_dim ** 2
        self.board = np.array([BLANK] * self.board_size)

        # Set corners to be borders
        self.board[0] = BORDER
        self.board[self.board_dim-1] = BORDER
        self.board[-self.board_dim] = BORDER
        self.board[-1] = BORDER

        # Set BLACK sides to contain BLACK pieces
        self.board[1:self.board_dim-1] = BLACK  # Left/top
        self.board[self.board_size-self.game_dim-1:-1] = BLACK  # Right/bottom

        # Set WHITE sides to contain WHITE pieces
        for i in range(self.board_dim,
                       self.board_dim*(self.board_dim-1),
                       self.board_dim):  # Left side
            self.board[i] = WHITE
        for i in range((self.board_dim*2)-1,
                       self.board_dim*(self.board_dim-1),
                       self.board_dim):  # Right side
            self.board[i] = WHITE

        self.current_player = BLACK

    def __str__(self) -> str:
        """Returns string representation of board."""

        char_reprs = {BLACK: "x", WHITE: "o", BORDER: "~", BLANK: "."}
        string = "  "
        for i in range(0, self.game_dim):
            string += chr(i+97) + " "
        string += "\n"
        for i in range(1, self.board_dim-1):
            string += " " * i
            string += str(i) + " "

            for j in range(1, self.board_dim-1):
                string += char_reprs[self.board[(i*self.board_dim)+j]] + " "
            string += "\n"

        return string

    def _2d_to_1d(self, index: list) -> int:
        """Converts 2d position to 1d position."""
        return (index[0]+1) * self.board_dim + index[1]+1

    def get_legal_moves(self) -> list:
        """Returns list of legal moves."""

        # TODO optimize
        legal_moves = []
        for i in range(len(self.board)):
            if self.board[i] == BLANK:
                legal_moves.append(i)
        return legal_moves

    def play_move(self, move: int, player: int = None) -> bool:
        """
        Play a move, update the current player, check for win.

        Parameters:
        move (int): Position of move
        player (int): WHITE or BLACK, player to move

        Returns:
        bool: True if game has been won
        """

        if type(move) is list:
            move = self._2d_to_1d(move)

        if player is None:
            player = self.current_player

        self.board[move] = player
        self.current_player = 3 - self.current_player  # Switch player

        return self._check_win(move)

    def clear_move(self, pos: int):
        """Set a tile at pos to BLANK."""

        if type(pos) is list:
            pos = self._2d_to_1d(pos)

        self.board[pos] = BLANK

    def _get_neighbours(self, move: int) -> list:
        """Returns a list of neighbours for a given move."""

        return [move-(self.board_dim),
                move-(self.board_dim-1),
                move-1,
                move+1,
                move+(self.board_dim-1),
                move+(self.board_dim)]

    def _check_win(self, move: int) -> bool:
        """
        Check if the game has been won.

        Does a DFS starting on move, moving to tiles of same color to
        check if move touches both sides of its color (win condition).

        Parameters:
        move (int): Position of move

        Returns:
        bool: True if the game has been won by player who made move
        """

        assert(self.board[move] == BLACK or self.board[move] == WHITE)

        stack = [move]
        visited = {str(move)}  # Don't add already searched moves to stack
        color = self.board[move]

        touch_left = False   # Is a move found on left side for player?
        touch_right = False  # Is a move found on right side for player?

        while len(stack) > 0:
            cur_move = stack.pop()

            if color == BLACK:
                if cur_move < self.board_dim:
                    if touch_right:
                        return True
                    touch_left = True
                    continue
                elif cur_move > self.board_size-self.board_dim:
                    if touch_left:
                        return True
                    touch_right = True
                    continue
            else:
                if cur_move % self.board_dim == 0:
                    if touch_right:
                        return True
                    touch_left = True
                    continue
                elif (cur_move+1) % self.board_dim == 0:
                    if touch_left:
                        return True
                    touch_right = True
                    continue

            neighbours = self._get_neighbours(cur_move)

            for n in neighbours:
                if not str(n) in visited and self.board[n] == color:
                    stack.append(n)
                    visited.add(str(n))

        return False

    def copy(self) -> "Hex1":
        """Return copy"""

        game_copy = Hex1(self.game_dim)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player

        return game_copy
