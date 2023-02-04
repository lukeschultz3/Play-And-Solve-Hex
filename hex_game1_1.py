# Created by Luke Schultz
# January 28, 2023

import numpy as np
from copy import deepcopy

import hex_game0
from hex_game0 import BLANK, BLACK, WHITE, BORDER

class Hex1_1(hex_game0.Hex):
    def __init__(self, size: int):
        super().__init__(size)
        self.size = size
        self.board = np.array([[BLANK] * size] * size)
        self.current_player = BLACK

    def copy(self):
        game_copy = Hex1_1(self.size)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player

        return game_copy
