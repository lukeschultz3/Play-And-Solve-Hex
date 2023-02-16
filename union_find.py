from copy import deepcopy
import numpy as np

from hex_game1 import Hex1, BLANK, BLACK, WHITE, BORDER

class Hex2():
    def __init__(self, game_dim: int, is_copy: bool=False):
        self.game_dim = game_dim
        self.board_dim = self.game_dim + 2
        self.board_size = self.board_dim ** 2
        self.board = np.array([BLANK] * self.board_size)

        #self.black_union_find = UnionFind(self.board_size)
        #self.white_union_find = UnionFind(self.board_size)
        #self.union_find = UnionFind(self.board_size)
        self.union_find = None

        if not is_copy:
            self.union_find = UnionFind(self.board_size)
            self.board[0] = BORDER
            self.board[self.board_dim-1] = BORDER
            self.board[-self.board_dim] = BORDER
            self.board[-1] = BORDER
            for i in range(1, self.board_dim-1):  # top row
                self.board[i] = BLACK

                if i > 1:
                    #self.black_union_find.union(i, i)
                    self.union_find.union(i-1, i)

            for i in range(self.board_size-self.game_dim-1, self.board_size-1):  # bottom row
                self.board[i] = BLACK

                if i > self.board_size-self.game_dim-1:
                    #self.black_union_find.union(i-1, i)
                    self.union_find.union(i-1, i)

            for i in range(self.board_dim, (self.board_dim-1)*self.board_dim, self.board_dim):  # left
                self.board[i] = WHITE
            
                if i > self.board_dim:
                    #self.white_union_find.union(i-self.board_dim, i)
                    self.union_find.union(i-self.board_dim, i)

            for i in range((self.board_dim*2)-1, (self.board_dim-1)*self.board_dim, self.board_dim):  # right
                self.board[i] = WHITE

                if i > (self.board_dim*2)-1:
                    #self.white_union_find.union(i-self.board_dim, i)
                    self.union_find.union(i-self.board_dim, i)

        self.current_player = BLACK
    
    def __str__(self) -> str:
        """ get string representation of board """
        char_reprs = {BLACK: "x", WHITE:"o", BORDER: "~", BLANK: "."}
        string = "  "
        for i in range(0, self.game_dim):
            string += chr(i+97) + " "
        string += "\n"
        for i in range(1, self.board_dim-1):
            string += " " * i
            string += str(i) + " "

            for j in range(1, self.board_dim-1):
                string += char_reprs[self.board[(i*self.board_dim)+j]] + " "
            string += "\n"
        
        return string
    
    def get_legal_moves(self) -> list:
        """ get list of legal moves """
        legal_moves = []
        for i in range(self.board_size):  # TODO: speedup
            if self.board[i] == BLANK:
                legal_moves.append(i)
        return legal_moves
    
    def play_move(self, move:int, player: int=None) -> bool:
        """ play a move and update the current player
        return True if the move won the game """

        if type(move) is list:  # 2d list
            # TODO test
            temp_move = (move[0]+1 * self.board_dim + move[1]+1)
            move = temp_move
        
        if player is None:
            player = self.current_player

        self.board[move] = player

        neighbours = self._get_neighbours(move)
        for neighbour_move in neighbours:
            if self.board[neighbour_move] == player:
                self.union_find.union(neighbour_move, move)
                """
                if player == BLACK:
                    self.black_union_find.union(neighbour_move, move)
                else:
                    self.white_union_find.union(neighbour_move, move)
                """
        
        self.current_player *= -1

        win = self.check_win()
        return win
    
    def clear_move(self, move:int):
        self.board[move] = BLANK
    
    def _get_neighbours(self, move: int) -> list:
        neighbours = [move-(self.board_dim),
                      move-(self.board_dim-1),
                      move-1,
                      move+1,
                      move+(self.board_dim-1),
                      move+(self.board_dim)]

        return neighbours

    def check_win(self):
        #if self.black_union_find.find(1) == self.black_union_find.find(self.board_size-2):
        if self.union_find.find(1) == self.union_find.find(self.board_size-2):
            return True
        
        #if self.white_union_find.find(self.board_dim) == self.white_union_find.find((self.board_dim*2)-1):
        if self.union_find.find(self.board_dim) == self.union_find.find((self.board_dim*2)-1):
            return True
        
        return False

    def copy(self):
        game_copy = Hex2(self.game_dim, is_copy=True)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player
        game_copy.union_find = deepcopy(self.union_find)
        #game_copy.black_union_find = deepcopy(self.black_union_find)
        #game_copy.white_union_find = deepcopy(self.white_union_find)

        return game_copy


class UnionFind():
    def __init__(self, size):
        self.parent_list = [i for i in range(size)]

    def union(self, x, y):
        #repr_x, rank_x = self.find(x)
        #repr_y, rank_y = self.find(y)
        repr_x = self.find(x)
        repr_y = self.find(y)

        if repr_x == repr_y:  # in same disjoin set
            return False

        self.parent_list[repr_x] = y

        """
        if rank_x <= rank_y:
            # TODO: test performance other way
            #self.parent_list[repr_y] = x
            self.parent_list[repr_x] = y
        else:
            #self.parent_list[repr_x] = y
            self.parent_list[repr_y] = x
        """

    def find(self, x):  # using grandparent compression
        #rank = 0
        while True:
            parent_x = self.parent_list[x]
            if x == parent_x:
                #return x, rank
                return x
            #rank += 1

            grandparent_x = self.parent_list[parent_x]
            if parent_x == grandparent_x:
                #return parent_x, rank
                return parent_x
            #rank += 1

            self.parent_list[x], x = grandparent_x, grandparent_x


if __name__=="__main__":
    game = Hex2(5)


    print(game.board)
    print(game)
    print(game.union_find.parent_list)
    print("win:", game.check_win())

    black_test_moves = [17, 23, 30, 31, 38,  9, 10]
    white_test_moves = [19, 25, 16, 24, 15, 22, 21]
    #for move in black_test_moves:
    for i in range(len(black_test_moves) + len(white_test_moves)):
        if i % 2 == 1:
            game.play_move(black_test_moves[i//2], BLACK)
        else:
            game.play_move(white_test_moves[i//2], WHITE)
        print(game)
        print(game.union_find.parent_list)
        print("win:", game.check_win())
        print("=============\n\n")
    
    for move in black_test_moves:
        print(move, game.union_find.find(move))

    """
    print(game.board)
    print(game)
    print(game.union_find.parent_list)
    print("win:", game.check_win())

    white_test_moves = [19, 25, 17, 24, 15, 22, 29, 23]
    for move in white_test_moves:
        game.play_move(move, WHITE)
        print(game)
        print(game.union_find.parent_list)
        print("win:", game.check_win())
        print("=============\n\n")

    for move in white_test_moves:
        print(move, game.union_find.find(move))
    """