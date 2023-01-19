# Created by Luke Schultz
# December 16, 2022

from copy import deepcopy
import numpy as np


# board constants
BLANK = 0
BLACK = 1
WHITE = -1
BORDER = 3


class Hex:
    def __init__(self, size: int):
        self.size = size
        self.board = np.array([BLANK for i in range(size * size)])
        #self.board = np.array([[BLANK for i in range(size)] for i in range(size)])
        self.legal_moves = np.array([True for i in range(size * size)])
        #self.legal_moves = np.array([[True for i in range(size)] for i in range(size)])
        self.current_player = BLACK

    def __str__(self) -> str:
        """ get string representation of board """
        string = " "

        for i in range(self.size):
            if i < 8:
                string += chr(97+i) + " "
            else:
                string += chr(97+i+1) + " "
        string += "\n"

        for i in range(self.size * self.size):
            if i % self.size == 0:
                if i // self.size < 9:  # single digit coord
                    string += " " * (i//self.size) + str((i//self.size)+1) + " "
                else:  # double digit coord
                    string += " " * ((i//self.size)-1) + str((i//self.size)+1) + " "

            if self.board[i] == BLACK:
                string += "x "
            elif self.board[i] == WHITE:
                string += "o "
            elif self.board[i] == BLANK:
                string += ". "
            else:
                string += str(self.board[i])

            if i % self.size == self.size-1:
                string += "\n"

        return string
                    
    def get_legal_moves(self) -> list:
        """ get list of legal moves """
        legal_moves = []
        for i in range(self.size * self.size):
            if self.legal_moves[i]:
                legal_moves.append(i)
        return legal_moves

    def play_move(self, move:int, player: int=None) -> bool:
        """ play a move and update the current player
        return True if the move won the game """
        assert(self.legal_moves[move])  # fail if illegal move

        if player != None:  # specific player given
            self.board[move] = player
        else:
            self.board[move] = self.current_player

        self.legal_moves[move] = False
        self.current_player *= -1  # switch player

        win = self._check_win(move)
        return win
    
    def clear_move(self, move:int):
        """ set a tile to BLANK,
        used for clearing a move """
        self.board[move] = BLANK
        self.legal_moves[move] = True

    def _get_neighbours(self, move: int) -> list:
        """ get list of neighbouring tiles """
        neighbours = [move-self.size,
                      move-(self.size-1),
                      move-1,
                      move+1,
                      move+(self.size-1),
                      move+self.size]

        return neighbours

    def _check_win(self, move) -> int:
        """ do a DFS search on adjacent tiles of same color to see if move
        touches both sides of it's color (win condition) """
        assert(self.board[move] == BLACK or self.board[move] == WHITE)

        stack = [move]  # maintains list of moves
        visited = {str(move)}  # don't add already searched moves to stack
        color = self.board[move]

        touch_left = False   # is a move found on left side for player?
        touch_right = False  # is a move found on right side for player?

        while len(stack) > 0:
            cur_move = stack.pop()

            if color == BLACK:
                if cur_move % self.size == 0:
                    if touch_right == True:
                        return True
                    touch_left = True
                elif cur_move % self.size == self.size-1:
                    if touch_left == True:
                        return True
                    touch_right = True
            else:
                if cur_move // self.size == 0:
                    if touch_right == True:
                        return True
                    touch_left = True
                elif cur_move // self.size == self.size-1:
                    if touch_left == True:
                        return True
                    touch_right = True

            neighbours = self._get_neighbours(cur_move)

            for n in neighbours:
                if (n % self.size >= 0 and n % self.size < self.size
                        and n // self.size >= 0 and n // self.size < self.size):
                    if not str(n) in visited and self.board[n] == color:
                        stack.append(n)
                        visited.add(str(n))

        return False

    def copy(self):
        game_copy = Hex(self.size)
        game_copy.board = deepcopy(self.board)
        game_copy.legal_moves = deepcopy(self.legal_moves)
        game_copy.current_player = self.current_player

        return game_copy


if __name__=="__main__":
    game = Hex(3)
    print(str(game))

    print(game.play_move([2,2]))
    print(str(game))

    print(game.play_move([2,0]))
    print(str(game))

    print(game.play_move([1,1]))
    print(str(game))

    print(game.play_move([0,2]))
    print(str(game))

    print(game.play_move([0,1]))
    print(str(game))

    print(game.play_move([2,1]))
    print(str(game))

    print(game.play_move([1,2]))
    print(str(game))
