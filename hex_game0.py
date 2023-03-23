# Created by Luke Schultz
# Fall 2022 / Winter 2023
#
# 2d list board representation.
# Board Representation:
# 0 0 0    0 0 0
# 0 0 0 ==  0 0 0
# 0 0 0      0 0 0
# Where BLANK = 0


from copy import deepcopy


# board constants
BLANK = 0
BLACK = 1
WHITE = 2
BORDER = 3


class Hex:
    def __init__(self, size: int):
        self.size = size
        self.board = [[BLANK for i in range(size)] for j in range(size)]
        self.current_player = BLACK

    def __str__(self) -> str:
        """Returns string representation of board."""

        string = " "

        for i in range(self.size):
            if i < 8:
                string += chr(97+i) + " "
            else:
                string += chr(97+i+1) + " "
        string += "\n"

        for i in range(self.size):
            if i < 9:  # Single digit coord
                string += " " * (i) + str(i+1) + " "
            else:  # Double digit coord
                string += " " * (i-1) + str(i+1) + " "

            for j in range(self.size):
                if self.board[i][j] == BLACK:
                    string += "x "
                elif self.board[i][j] == WHITE:
                    string += "o "
                elif self.board[i][j] == BLANK:
                    string += ". "
                else:
                    string += str(self.board[i][j]) + " "
            string += "\n"

        return string

    def get_legal_moves(self) -> list:
        """Returns list of legal moves."""

        # TODO optimize
        legal_moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == BLANK:
                    legal_moves.append([i, j])
        return legal_moves

    def play_move(self, move: list, player: int = None) -> bool:
        """
        Play a move, update the current player, check for win.

        Parameters:
        move(list): Position of move
        player (int): WHITE or BLACK, player to move

        Returns:
        bool: True if game has been won
        """

        if type(move) is int:  # Convert 1d move to 2d
            move = [move // (self.size+1), move % (self.size+1)]

        if player is None:
            player = self.current_player

        self.board[move[0]][move[1]] = player
        self.current_player = 3 - self.current_player  # Switch player

        return self._check_win(move)

    def clear_move(self, move: list):
        """Set a tile to BLANK."""

        self.board[move[0]][move[1]] = BLANK

    def _get_neighbours(self, move: list) -> list:
        """Returns a list of neighbouring tiles."""

        return [[move[0],   move[1]-1],
                [move[0]+1, move[1]-1],
                [move[0]-1, move[1]],
                [move[0]+1, move[1]],
                [move[0]-1, move[1]+1],
                [move[0],   move[1]+1]]

    def _check_win(self, move: list) -> int:
        """
        Check if the game has been won.

        Does a DFS starting on move, moving to tiles of same color to
        check if move touches both sides of its color (win condition).

        Parameters:
        move (int): Position of move

        Returns:
        bool: True if the game has been won by player who made move
        """

        assert(self.board[move[0]][move[1]] == BLACK
               or self.board[move[0]][move[1]] == WHITE)

        stack = [move]
        visited = {str(move)}  # Don't add already searched moves to stack
        color = self.board[move[0]][move[1]]

        touch_left = False   # Is a move found on left side for player?
        touch_right = False  # Is a move found on right side for player?

        while len(stack) > 0:
            cur_move = stack.pop()

            if color == BLACK:
                if cur_move[0] == 0:
                    if touch_right:
                        return True
                    touch_left = True
                elif cur_move[0] == self.size-1:
                    if touch_left:
                        return True
                    touch_right = True
            else:
                if cur_move[1] == 0:
                    if touch_right:
                        return True
                    touch_left = True
                elif cur_move[1] == self.size-1:
                    if touch_left:
                        return True
                    touch_right = True

            neighbours = self._get_neighbours(cur_move)

            for n in neighbours:
                if (n[0] >= 0 and n[0] < self.size
                        and n[1] >= 0 and n[1] < self.size):
                    if (not str(n) in visited
                            and self.board[n[0]][n[1]] == color):
                        stack.append(n)
                        visited.add(str(n))

        return False

    def copy(self) -> "Hex":
        """Return copy"""

        game_copy = Hex(self.size)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player

        return game_copy


if __name__ == "__main__":
    game = Hex(3)
    print(str(game))

    print(game.play_move([2, 2]))
    print(str(game))

    print(game.play_move([2, 0]))
    print(str(game))

    print(game.play_move([1, 1]))
    print(str(game))

    print(game.play_move([0, 2]))
    print(str(game))

    print(game.play_move([0, 1]))
    print(str(game))

    print(game.play_move([2, 1]))
    print(str(game))

    print(game.play_move([1, 2]))
    print(str(game))
