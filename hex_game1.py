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


class Hex1:
    def __init__(self, board_side_len: int):
        self.board_side_len = board_side_len
        self.side_len_with_buffer = board_side_len + 1
        self.game_size = board_side_len ** 2
        self.board_size = (self.board_side_len+2) * self.side_len_with_buffer

        self.board = np.array([BLANK] * self.board_size)

        # add borders
        self.board[0:self.side_len_with_buffer] = BORDER
        self.board[len(self.board)-self.board_side_len-1:] = BORDER
        for i in range(1, self.board_side_len+2):
            self.board[i*(self.side_len_with_buffer)-1] = BORDER
        
        self.current_player = BLACK

    def __str__(self) -> str:
        """ get string representation of board """
        string = " "

        for i in range(self.board_side_len):
            if i < 8:
                string += chr(97+i) + " "
            else:
                string += chr(97+i+1) + " "
        string += "\n"

        i = self.side_len_with_buffer
        added_so_far = 0
        while added_so_far < self.game_size:
            if added_so_far % self.board_side_len == 0:
                if added_so_far // self.board_side_len < 9:  # single digit coord
                    string += (" " * (added_so_far//self.board_side_len)
                               + str((added_so_far//self.board_side_len)+1)
                               + " ")
                else:  # double digit coord
                    string += (" " * ((added_so_far//self.board_side_len)-1)
                               + str((added_so_far//self.board_side_len)+1)
                               + " ")

            if self.board[i] == BORDER:
                pass
            elif self.board[i] == BLACK:
                string += "x "
                added_so_far += 1
            elif self.board[i] == WHITE:
                string += "o "
                added_so_far += 1
            elif self.board[i] == BLANK:
                string += ". "
                added_so_far += 1
            else:
                string += str(self.board[i])
                added_so_far += 1

            if added_so_far % self.board_side_len == 0:
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

        if type(move) is list:  # 2d list
            temp_move = (move[0]+1) * self.side_len_with_buffer + move[1]
            move = temp_move

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
        neighbours = [move-(self.board_side_len+1),
                      move-self.board_side_len,
                      move-1,
                      move+1,
                      move+self.board_side_len,
                      move+self.board_side_len+1]

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
            normalized_move = cur_move - self.board_side_len

            if color == BLACK:
                if normalized_move // (self.side_len_with_buffer) == 0:
                    if touch_right == True:
                        return True
                    touch_left = True
                elif normalized_move // (self.side_len_with_buffer) == self.board_side_len-1:
                    if touch_left == True:
                        return True
                    touch_right = True
            else:
                if normalized_move % (self.side_len_with_buffer) == 1:
                    if touch_right == True:
                        return True
                    touch_left = True
                elif normalized_move % (self.side_len_with_buffer) == self.board_side_len:
                    if touch_left == True:
                        return True
                    touch_right = True

            neighbours = self._get_neighbours(cur_move)

            for n in neighbours:
                if not str(n) in visited and self.board[n] == color:
                    stack.append(n)
                    visited.add(str(n))

        return False

    def copy(self):
        game_copy = Hex1(self.board_side_len)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player

        return game_copy
