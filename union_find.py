
from hex_game1 import Hex1, BLANK, BLACK, WHITE, BORDER

class Hex2(Hex1):
    def __init__(self, board_side_len: int):
        super().__init__(board_side_len)
        self.black_union_find = UnionFind(self.board_size)
        self.white_union_find = UnionFind(self.board_size)
    
    def play_move(self, move, player):

        if type(move) is list:  # 2d list
            temp_move = (move[0]+1) * self.side_len_with_buffer + move[1]
            move = temp_move

        self.board[move] = player

        if player == BLACK:
            self.black_union_find.add_new_set(move)
        else:
            self.white_union_find.add_new_set(move)

        touch_border = False

        neighbours = self._get_neighbours(move)
        for neighbour_move in neighbours:
            if self.board[neighbour_move] == player:
                if player == BLACK:
                    self.black_union_find.union(neighbour_move, move)
                else:
                    self.white_union_find.union(neighbour_move, move)
            elif not touch_border and self.board[neighbour_move] == BORDER:
                if player == BLACK:
                    if neighbour_move < self.side_len_with_buffer:
                        self.black_union_find.left_parents.add(move)
                        touch_border = True
                    elif (neighbour_move >=
                            self.board_size - (self.side_len_with_buffer-1)):
                        self.black_union_find.right_parents.add(move)
                        touch_border = True
                else:
                    if (self.side_len_with_buffer < neighbour_move < 
                            self.board_size - (self.side_len_with_buffer-1)
                            and (neighbour_move+1) % self.side_len_with_buffer == 0):
                        if (move+2) % self.side_len_with_buffer == 0:
                            self.white_union_find.right_parents.add(move)
                            touch_border = True
                        else:
                            self.white_union_find.left_parents.add(move)
                            touch_border = True
    
    def check_win(self):
        left_repr_set = set()
        for i in self.black_union_find.left_parents:
            left_repr_set.add(self.black_union_find.find(i)[0])
        
        for i in self.black_union_find.right_parents:
            if self.black_union_find.find(i)[0] in left_repr_set:
                return True
        
        left_repr_set = set()
        for i in self.white_union_find.left_parents:
            left_repr_set.add(self.white_union_find.find(i)[0])
        
        for i in self.white_union_find.right_parents:
            if self.white_union_find.find(i)[0] in left_repr_set:
                return True
        
        return False

class UnionFind():
    def __init__(self, size):
        self.parent_list = [None] * size
        #self.repr_connect_left = set()   # all reprs that are connected to left are contained in this set
        #self.repr_connect_right = set()  # all reprs that are connected to right are contained in this set
        self.left_parents = set()
        self.right_parents = set()

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


    """
    print(game.board)
    print(game)
    print(game.black_union_find.parent_list)
    print("top parents:", game.black_union_find.left_parents)
    print("bottom parents:", game.black_union_find.right_parents)
    print("win:", game.check_win())

    black_test_moves = [8, 9, 20, 21, 14, 31, 26]
    for move in black_test_moves:
        game.play_move(move, BLACK)
        print(game)
        print(game.black_union_find.parent_list)
        print("top parents:", game.black_union_find.left_parents)
        print("bottom parents:", game.black_union_find.right_parents)
        print("win:", game.check_win())

    print(game.black_union_find.find(8))
    print(game.black_union_find.find(9))
    print(game.black_union_find.find(20))
    print(game.black_union_find.find(21))
    print(game.black_union_find.find(14))
    """

    print(game.board)
    print(game)
    print(game.white_union_find.parent_list)
    print("top parents:", game.white_union_find.left_parents)
    print("bottom parents:", game.black_union_find.right_parents)
    print("win:", game.check_win())

    white_test_moves = [16, 21, 14, 20, 12, 18, 24, 19]
    for move in white_test_moves:
        game.play_move(move, WHITE)
        print(game)
        print(game.white_union_find.parent_list)
        print("top parents:", game.white_union_find.left_parents)
        print("bottom parents:", game.white_union_find.right_parents)
        print("win:", game.check_win())
        print("=============\n\n")

    for move in white_test_moves:
        print(move, game.white_union_find.find(move))
