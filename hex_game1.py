# Created by Luke Schultz
# December 16, 2022
# January 19, 2023

from copy import deepcopy
import numpy as np


# board constants
BLANK = 0
BLACK = 1
WHITE = -1
BORDER = 3


class Hex:
    def __init__(self, side_length: int):
        self.side_length = side_length
        self.game_size = side_length ** 2
        self.board_size = (self.side_length+2) * (self.side_length+1)

        self.board = np.array([BLANK for i in range(self.board_size)])
        self.board[0:self.side_length+1] = BORDER
        self.board[len(self.board)-self.side_length-1:] = BORDER
        for i in range(1, self.side_length+2):
            self.board[i*(self.side_length+1)-1] = BORDER

        self.current_player = BLACK

    def __str__(self) -> str:
        """ get string representation of board """
        string = " "

        for i in range(self.side_length):
            if i < 8:
                string += chr(97+i) + " "
            else:
                string += chr(97+i+1) + " "
        string += "\n"

        i = self.side_length+1
        printed_so_far = 0
        while printed_so_far < self.game_size:
            if printed_so_far % self.side_length == 0:
                if printed_so_far // self.side_length < 9:  # single digit coord
                    string += " " * (printed_so_far//self.side_length) + str((printed_so_far//self.side_length)+1) + " "
                else:  # double digit coord
                    string += " " * ((printed_so_far//self.side_length)-1) + str((printed_so_far//self.side_length)+1) + " "

            if self.board[i] == BORDER:
                pass
            elif self.board[i] == BLACK:
                string += "x "
                printed_so_far += 1
            elif self.board[i] == WHITE:
                string += "o "
                printed_so_far += 1
            elif self.board[i] == BLANK:
                string += ". "
                printed_so_far += 1
            else:
                string += str(self.board[i])
                printed_so_far += 1

            if printed_so_far % self.side_length == 0:
                i += 2
                string += "\n"
            else:
                i += 1

        return string
                    
    def get_legal_moves(self) -> list:
        """ get list of legal moves """
        legal_moves = []
        for i in range(len(self.board)):
            if self.board[i] == BLANK:
                legal_moves.append(i)
        return legal_moves

    def play_move(self, move:int, player: int=None) -> bool:
        """ play a move and update the current player
        return True if the move won the game """

        if player != None:  # specific player given
            self.board[move] = player
        else:
            self.board[move] = self.current_player

        self.current_player *= -1  # switch player

        win = self._check_win(move)
        return win
    
    def clear_move(self, move:int):
        """ set a tile to BLANK,
        used for clearing a move """
        self.board[move] = BLANK

    def _get_neighbours(self, move: int) -> list:
        """ get list of neighbouring tiles """
        neighbours = [move-(self.side_length+1),
                      move-self.side_length,
                      move-1,
                      move+1,
                      move+self.side_length,
                      move+self.side_length+1]

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
            normalized_move = cur_move - self.side_length

            if color == BLACK:
                #if cur_move % self.side_length == 0:
                if normalized_move // (self.side_length+1) == 0:
                    if touch_right == True:
                        return True
                    touch_left = True
                #elif cur_move % self.side_length == self.side_length-1:
                elif normalized_move // (self.side_length+1) == self.side_length-1:
                    if touch_left == True:
                        return True
                    touch_right = True
            else:
                #if cur_move // self.side_length == 0:
                if normalized_move % (self.side_length+1) == 1:
                    if touch_right == True:
                        return True
                    touch_left = True
                #elif cur_move // self.side_length == self.side_length-1:
                elif normalized_move % (self.side_length+1) == self.side_length:
                    if touch_left == True:
                        return True
                    touch_right = True

            neighbours = self._get_neighbours(cur_move)

            for n in neighbours:
                if not str(n) in visited and self.board[n] == color:
                    stack.append(n)
                    visited.add(str(n))

                """
                if (n >= 0 and n < self.side_length
                        and n // self.side_length >= 0 and n // self.side_length < self.side_length):
                    if not str(n) in visited and self.board[n] == color:
                        stack.append(n)
                        visited.add(str(n))
                """

        return False

    def copy(self):
        game_copy = Hex(self.side_length)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player

        return game_copy
