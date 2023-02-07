
from hex_game1 import Hex1, BLANK, BLACK, WHITE, BORDER

class Hex2(Hex1):
    def __init__(self, board_side_len: int):
        super().__init__(board_side_len)
        self.black_union_find = UnionFind(self.board_size)
        self.white_union_find = UnionFind(self.board_size)
    
    def play_move(self, move, player):
        self.board[move] = player

        if player == BLACK:
            self.black_union_find.add_new_set(move)
        else:
            self.white_union_find.add_new_set(move)

        neighbours = self._get_neighbours(move)
        for neighbour_move in neighbours:
            if self.board[neighbour_move] == player:
                if player == BLACK:
                    self.black_union_find.union(neighbour_move, move)
                else:
                    self.white_union_find.union(neighbour_move, move)
    
    def check_win(self, move):
        pass

class UnionFind():
    def __init__(self, size):
        self.parent_list = [None] * size
        self.repr_connect_left = set()   # all reprs that are connected to left are contained in this set
        self.repr_connect_right = set()  # all reprs that are connected to right are contained in this set

    def add_new_set(self, x):
        self.parent_list[x] = x

    def union(self, x, y):
        repr_x, rank_x = self.find(x)
        repr_y, rank_y = self.find(y)

        if repr_x == repr_y:  # in same disjoin set
            return False
        
        if rank_x <= rank_y:
            # TODO: test performance other way
            self.parent_list[repr_y] = x
        else:
            self.parent_list[repr_x] = y

    def find(self, x):  # using grandparent compression
        rank = 0
        while True:
            parent_x = self.parent_list[x]
            if x == parent_x:
                return x, rank
            rank += 1

            grandparent_x = self.parent_list[parent_x]
            if parent_x == grandparent_x:
                return parent_x, rank
            rank += 1

            self.parent_list[x], x = grandparent_x, grandparent_x


if __name__=="__main__":
    game = Hex2(5)
    print(game.board)
    print(game)
    print(game.black_union_find.parent_list)

    game.play_move(8, BLACK)
    print(game)
    print(game.black_union_find.parent_list)

    game.play_move(9, BLACK)
    print(game)
    print(game.black_union_find.parent_list)

    game.play_move(20, BLACK)
    print(game)
    print(game.black_union_find.parent_list)

    game.play_move(21, BLACK)
    print(game)
    print(game.black_union_find.parent_list)

    game.play_move(14, BLACK)
    print(game)
    print(game.black_union_find.parent_list)

    print(game.black_union_find.find(8))
    print(game.black_union_find.find(9))
    print(game.black_union_find.find(20))
    print(game.black_union_find.find(21))
    print(game.black_union_find.find(14))