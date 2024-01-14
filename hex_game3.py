# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot
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

from hex_game0 import Hex0, BLANK, BLACK, WHITE, BORDER
from union_find import UnionFind


class Hex3(Hex0):
    def __init__(self, game_dim: int, is_copy: bool = False):
        self.game_dim = game_dim
        self.board_dim = self.game_dim + 2
        self.board_size = self.board_dim ** 2
        self.board = np.array([BLANK] * self.board_size)

        self.current_player = BLACK
        self.block_union_find = None    # tracks the true blocks
        self.virtual_union_find = None  # tracks virtual connections
        self.carrier_pairs = {BLACK: {}, WHITE: {}}

        if not is_copy:
            self.block_union_find = UnionFind(self.board_size)
            self.virtual_union_find = UnionFind(self.board_size)
            self.board[0] = BORDER
            self.board[self.board_dim-1] = BORDER
            self.board[-self.board_dim] = BORDER
            self.board[-1] = BORDER

            # Initialize top row
            for i in range(1, self.board_dim-1):
                self.board[i] = BLACK
                if i > 1:
                    self.block_union_find.union(i-1, i)
                    self.virtual_union_find.union(i-1, i)

            # Initialize bottom row
            for i in range(self.board_size-self.game_dim-1, self.board_size-1):
                self.board[i] = BLACK
                if i > self.board_size-self.game_dim-1:
                    self.block_union_find.union(i-1, i)
                    self.virtual_union_find.union(i-1, i)

            # Initialize left side
            for i in range(self.board_dim,
                           (self.board_dim-1)*self.board_dim,
                           self.board_dim):
                self.board[i] = WHITE
                if i > self.board_dim:
                    self.block_union_find.union(i-self.board_dim, i)
                    self.virtual_union_find.union(i-self.board_dim, i)

            # Initialize right side
            for i in range((self.board_dim*2)-1,
                           (self.board_dim-1)*self.board_dim,
                           self.board_dim):
                self.board[i] = WHITE
                if i > (self.board_dim*2)-1:
                    self.block_union_find.union(i-self.board_dim, i)
                    self.virtual_union_find.union(i-self.board_dim, i)

    def get_simulation_moves(self, player) -> list:
        """Returns list of moves for simulations,
           excluding carriers of players VC."""
        
        for carrier_stone in self.carrier_pairs[player].keys():
            if self.board[carrier_stone] != None:
                simulation_moves = [self.carrier_pairs[player][carrier_stone]]
                del self.carrier_pairs[player][self.carrier_pairs[player][carrier_stone]]
                del self.carrier_pairs[player][carrier_stone]
                return simulation_moves

        simulation_moves = []
        for i in range(len(self.board)):
            if self.board[i] == BLANK and i not in self.carrier_pairs[player]:
                simulation_moves.append(i)
        return simulation_moves

    def _get_virtual_neighbours(self, move: int) -> list:
        """ Returns a list of the cells that can possible be virtually
            connected to move. """
        
        virtual_neighbours = {
            move - (self.board_dim + 1):  (move-(self.board_dim), move-1),
            move - (2 * self.board_dim + 1): (move-(self.board_dim), move-(self.board_dim-1)),
            move - (self.board_dim + 1): (move+(self.board_dim-1), move+1),
            move + (self.board_dim + 1): (move+1, move+(self.board_dim)),
            move + (2 * self.board_dim + 1): (move+(self.board_dim), move+(self.board_dim-1)),
            move + (self.board_dim + 1): (move-1, move+(self.board_dim-1)),
        }

        return virtual_neighbours

    def play_move(self, move: int, player: int = None) -> bool:
        """
        Play a move, update the current player, check for win.

        Parameters:
        move (int): Position of move
        player (int): WHITE or BLACK, player to move
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
                self.block_union_find.union(neighbour_move, move)
                self.virtual_union_find.union(neighbour_move, move)

        virtual_neighbours = self._get_virtual_neighbours(move)
        for neighbour_move in virtual_neighbours.keys():
            carrier1, carrier2 = virtual_neighbours[neighbour_move]
            try:
                if (self.board[neighbour_move] == player
                        and self.board[carrier1] == None
                        and self.board[carrier2] == None
                        and carrier1 not in self.carriers[player]
                        and carrier2 not in self.carriers[player]):
                    self.virtual_union_find.union(neighbour_move, move)
                    self.carriers[player][carrier1] = carrier2
                    self.carriers[player][carrier2] = carrier1
            except IndexError:
                continue

    def check_win(self, *args) -> bool:
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

        """
        if self.block_union_find.find(1) == self.block_union_find.find(self.board_size-2):
            return True

        if (self.block_union_find.find(self.board_dim)
                == self.block_union_find.find((self.board_dim*2)-1)):
            return True
        """

        if self.virtual_union_find.find(1) == self.virtual_union_find.find(self.board_size-2):
            return True

        if (self.virtual_union_find.find(self.board_dim)
                == self.virtual_union_find.find((self.board_dim*2)-1)):
            return True

        return False
    
    def check_true_win(self, *args) -> bool:
        if self.block_union_find.find(1) == self.block_union_find.find(self.board_size-2):
            return True

        if (self.block_union_find.find(self.board_dim)
                == self.block_union_find.find((self.board_dim*2)-1)):
            return True
        
        return False
 
    def copy(self) -> "Hex3":
        """Return copy"""

        game_copy = Hex3(self.game_dim, is_copy=True)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player
        game_copy.block_union_find = deepcopy(self.block_union_find)
        game_copy.virtual_union_find = deepcopy(self.virtual_union_find)

        return game_copy
