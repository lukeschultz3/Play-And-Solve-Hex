# Created by Luke Schultz
# January 28, 2023

import numpy as np

import hex_game0
from hex_game0 import BLANK

class Hex1_1(hex_game0.Hex):
    def __init__(self, size: int):
        super()
        self.board = np.array([[BLANK] * size] * size)

