# Created by Luke Schultz
# Winter 2023
#
# 1d numpy array board representation.
# Board Representation:
# 3 1 1 1 3    3 1 1 1 3
# 2 0 0 0 2     2 0 0 0 2
# 2 0 0 0 2 ==   2 0 0 0 2
# 2 0 0 0 2       2 0 0 0 2
# 3 1 1 1 3        3 1 1 1 3
# Where BOARDER = 3, BLACK = 1, WHITE = 2, BLANK = 0


from copy import deepcopy
import numpy as np

from hex_game1 import Hex1, BLANK, BLACK, WHITE, BORDER
from union_find import UnionFind


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

        return self._check_win()

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
    
    def compute_black_vc(self, stone: list):
        """Compute simple virutal connections for a black stone on the board"""

        row = stone[0]
        col = stone[1]
        vcs = []

        # Check if the stone is in the top left corner of the board.
        # If it is, that means it only has a bridge connection to the lower right cell.
        if col == 0 and row == 0:
            lower_right_vc = [row + 1, col]
            vcs.append(lower_right_vc)
        
        # Check if the stone is in the bottom right corner of the board. 
        # If it is, that means it only has a bridge connection to the upper left cell.
        elif col == (self.board_dim - 3) and row == (self.board_dim - 3):
            upper_left_vc = [row - 1, col]
            vcs.append(upper_left_vc)
        
        # Check if the stone is in the first row of the board, but not the first left/right corners.
        # If it is, that means it only has a bridge connection to the lower left/right cells.
        elif row == 0 and row != col and col != (self.board_dim - 3):
            lower_left_vc = [row + 1, col - 1]
            lower_right_vc = [row + 1, col]
            left_vc = [row, col - 1]
            right_vc = [row, col + 1]
            vcs.append(lower_left_vc)
            vcs.append(lower_right_vc)
            vcs.append(left_vc)
            vcs.append(right_vc)
        
        # Check if the stone is in the top right corner of the board.
        # If it is, that means it only has a bridge connection to the left, lower left, and lower right cells.
        elif row == 0 and col == (self.board_dim - 3):
            lower_left_vc = [row + 1, col - 1]
            lower_right_vc = [row + 1, col]
            left_vc = [row, col - 1]
            vcs.append(lower_left_vc)
            vcs.append(lower_right_vc)
            vcs.append(left_vc)
        
        # Check if the stone is in the bottom left corner of the board.
        #If it is, that means it only has a bridge connection to the right, upper left, and upper right cells.
        elif row == (self.board_dim - 3) and col == 0:
            upper_left_vc = [row - 1, col]
            upper_right_vc = [row - 1, col + 1]
            right_vc = [row, col + 1]
            vcs.append(upper_left_vc)
            vcs.append(upper_right_vc)
            vcs.append(right_vc)

        # Check if the stone is in the bottom row of the board, but not the bottom left/right corners.
        # If it is, that means it only has a bridge connection to the upper left/right cells.
        elif row == (self.board_dim - 3) and row != col and col != (self.board_dim - 3):
            upper_left_vc = [row - 1, col]
            upper_right_vc = [row - 1, col + 1]
            left_vc = [row, col - 1]
            right_vc = [row, col + 1]
            vcs.append(upper_left_vc)
            vcs.append(upper_right_vc)
            vcs.append(left_vc)
            vcs.append(right_vc)
        
        # Check if the stone is in the leftmost edge of the board but not the top/bottom left corner.
        # If it is, it will be missing a left and lower left bridge connection.
        elif col == 0 and row != col and row != (self.board_dim - 3):
            upper_left_vc = [row - 1, col]
            upper_right_vc = [row - 1, col + 1]
            lower_right_vc = [row + 1, col]
            right_vc = [row, col + 1]
            vcs.append(upper_left_vc)
            vcs.append(upper_right_vc)
            vcs.append(lower_right_vc)
            vcs.append(right_vc)
        
        # Check if the stone is in the rightmost edge of the board but not the top/bottom right corner.
        # If it is, it will be missing an upper right bridge connection.
        elif col == (self.board_dim - 3) and row != 0 and row != col:
            upper_left_vc = [row - 1, col]
            lower_left_vc = [row + 1, col - 1]
            lower_right_vc = [row + 1, col]
            left_vc = [row, col - 1]
            vcs.append(upper_left_vc)
            vcs.append(lower_left_vc)
            vcs.append(lower_right_vc)
            vcs.append(left_vc)

        # The stone is not in the edges of the board.
        # This means it has a bridge connection to all combinations of upper/lower/left/right cells.
        else:
            upper_left_vc = [row - 1, col]
            upper_right_vc = [row - 1, col + 1]
            lower_left_vc = [row + 1, col - 1]
            lower_right_vc = [row + 1, col]
            left_vc = [row, col - 1]
            right_vc = [row, col + 1]
            vcs.append(upper_left_vc)
            vcs.append(upper_right_vc)
            vcs.append(lower_left_vc)
            vcs.append(lower_right_vc)
            vcs.append(left_vc)
            vcs.append(right_vc)

        # Return the final list of virtual connections.
        return vcs
    
    def check_black_vcs(self, stone_1: list, stone_2: list):
        """Check if two stones on the board share a simple bridge connection.
        This is also known as a Hex virtual connection."""

        # The compute_black_vc function will return a 2D list.
        # 2D lists in python aren't hashable so I need to turn these into a hashmap of tuples first.
        stone_1_vcs = map(tuple, self.compute_black_vc(stone_1))
        stone_2_vcs = map(tuple, self.compute_black_vc(stone_2))

        # We turn the hashmaps into sets and then calculate the intersection.
        # This finds if stone_1 has common neighbours with stone_2.
        common_vcs = set(stone_1_vcs).intersection(set(stone_2_vcs))

        # If there is more than 1 common neighbour, that means a bridge connection exists. 
        if len(common_vcs) > 1:
            return common_vcs
        
        # If there is 0 or only 1 common neighbour, there is no simple bridge.
        else:
            return {}
    