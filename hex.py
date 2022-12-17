# Created by Luke Schultz
# December 16, 2022


# board constants
BLANK = 0
BLACK = 1
WHITE = 2
BORDER = 3


class Hex:
    def __init__(self, size):
        self.size = size
        self.board = [[BLANK for i in range(size)] for i in range(size)]
        self.legal_moves = [[True for i in range(size)] for i in range(size)]
        self.current_player = BLACK

    def __str__(self):
        """ get string representation of board """
        string = ""
        for i in range(self.size):
            string += " " * i
            for j in range(self.size):
                string += str(self.board[i][j]) + " "
            string += "\n"

        return string

    def play_move(self, move, player = None):
        assert(self.legal_moves[move[0]][move[1]])  # fail if illegal move

        if player != None:  # specific player given
            self.board[move[0]][move[1]] = player
            self.legal_moves[move[0]][move[1]] = False

            if player == BLACK:  # TODO: one liner
                self.current_player = WHITE
            else:
                self.current_player = BLACK
        else:
            self.board[move[0]][move[1]] = self.current_player
            self.legal_moves[move[0]][move[1]] = False

            if self.current_player == BLACK:
                self.current_player = WHITE
            else:
                self.current_player = BLACK

        win = self._check_win(move)
        
        return win

    def _get_neighbours(self, move):
        neighbours = [[move[0],   move[1]-1],
                      [move[0]+1, move[1]-1],
                      [move[0]-1, move[1]],
                      [move[0]+1, move[1]],
                      [move[0]-1, move[1]+1],
                      [move[0],   move[1]+1]]

        return neighbours

    def _check_win(self, move):
        assert(self.board[move[0]][move[1]] == BLACK
                   or self.board[move[0]][move[1]] == WHITE)

        stack = [move]  # maintains list of moves
        visited = {str(move)}
        color = self.board[move[0]][move[1]]

        touch_left = False   # is a move found on left side for player?
        touch_right = False  # is a move found on right side for player?

        while len(stack) > 0:
            cur_move = stack.pop()

            if color == BLACK:
                if cur_move[0] == 0:
                    if touch_right == True:
                        return True
                    touch_left = True
                elif cur_move[0] == self.size-1:
                    if touch_left == True:
                        return True
                    touch_right = True
            else:
                if cur_move[1] == 0:
                    if touch_right == True:
                        return True
                    touch_left = True
                elif cur_move[1] == self.size-1:
                    if touch_left == True:
                        return True
                    touch_right = True

            neighbours = self._get_neighbours(cur_move)

            for n in neighbours:
                if n[0] >= 0 and n[0] < self.size and n[1] >= 0 and n[1] < self.size:
                    if not str(n) in visited and self.board[n[0]][n[1]] == color:
                        stack.append(n)
                        visited.add(str(n))

        return False


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
