from copy import deepcopy
import numpy as np

from hex_game1 import Hex1, BLANK, BLACK, WHITE, BORDER


class Hex2(Hex1):
    def __init__(self, game_dim: int, is_copy: bool = False):
        self.game_dim = game_dim
        self.board_dim = self.game_dim + 2
        self.board_size = self.board_dim ** 2
        self.board = np.array([BLANK] * self.board_size)

        self.current_player = BLACK
        self.union_find = None

        if not is_copy:
            self.union_find = UnionFind(self.board_size)
            self.board[0] = BORDER
            self.board[self.board_dim-1] = BORDER
            self.board[-self.board_dim] = BORDER
            self.board[-1] = BORDER

            # Initialize top row
            for i in range(1, self.board_dim-1):
                self.board[i] = BLACK
                if i > 1:
                    self.union_find.union(i-1, i)

            # Initialize bottom row
            for i in range(self.board_size-self.game_dim-1, self.board_size-1):
                self.board[i] = BLACK
                if i > self.board_size-self.game_dim-1:
                    self.union_find.union(i-1, i)

            # Initialize left side
            for i in range(self.board_dim,
                           (self.board_dim-1)*self.board_dim,
                           self.board_dim):
                self.board[i] = WHITE
                if i > self.board_dim:
                    self.union_find.union(i-self.board_dim, i)

            # Initialize right side
            for i in range((self.board_dim*2)-1,
                           (self.board_dim-1)*self.board_dim,
                           self.board_dim):
                self.board[i] = WHITE
                if i > (self.board_dim*2)-1:
                    self.union_find.union(i-self.board_dim, i)

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

        neighbours = self._get_neighbours(move)
        for neighbour_move in neighbours:
            if self.board[neighbour_move] == player:
                self.union_find.union(neighbour_move, move)

        return self._check_win(move)

    def _check_win(self) -> bool:
        """
        Check if the game has been won.

        Uses Union Find data structure to check if two sides of the
        same color are in the same set (i.e. touching).

        Since this function is called only in the play_move function,
        we only need to consider if the game has been won, not who
        has won it. The player who made the last move is known by
        play_move, and will be the winner if the game has been won.

        Returns:
        bool: True if the game has been won
        """
        if self.union_find.find(1) == self.union_find.find(self.board_size-2):
            return True

        if (self.union_find.find(self.board_dim)
                == self.union_find.find((self.board_dim*2)-1)):
            return True

        return False

    def copy(self) -> "Hex1":
        """Return copy"""

        game_copy = Hex2(self.game_dim, is_copy=True)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player
        game_copy.union_find = deepcopy(self.union_find)

        return game_copy


class UnionFind():
    def __init__(self, size):
        self.parent_list = [i for i in range(size)]

    def union(self, x: int, y: int) -> bool:
        """
        Joins two sets

        Parameters:
        x (int): member of one set
        y (int): member of (possibly) another set

        Returns:
        bool: False if x, y were in the same set prior to function call,
              True otherwise
        """

        repr_x = self.find(x)
        repr_y = self.find(y)

        if repr_x == repr_y:  # In the same disjoint set
            return False

        self.parent_list[repr_x] = y
        return True

    def find(self, x: int) -> int:
        """
        Find the repr of an element.

        Uses grandparent compression to speed up execution.

        Parameters:
        x (int): element to find repr of

        Returns:
        int: repr of x
        """

        while True:
            parent_x = self.parent_list[x]
            if x == parent_x:
                return x

            grandparent_x = self.parent_list[parent_x]
            if parent_x == grandparent_x:
                return parent_x

            # grandparent compression:
            self.parent_list[x], x = grandparent_x, grandparent_x
