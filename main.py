import hex_game0
import hex_game1
import hex_game1_1
import hex_game2
from hex_game0 import BLACK, WHITE, BLANK
import mcts0
import mcts1
import pns0
import cProfile

# TO DO:
# • Check potential virtual connections in random order
# • You can only be VCs with 1 other stone. 2 VCs involving the same stone is redundant.
# • Change the simulations code to acknowledge when the opponent has moved inside of an existing virtual connection.

size = 7
previous_game = None
version = "2"  # "0" or "1" or "1.1" or "2"

def coord_to_move(coord: str) -> list:
    """convert coord in the form a1 to list index"""
    try:
        col = ord(coord[0]) - 97
        if col >= 9:
            col -= 1
        row = int(coord[1:])-1
        
        return [row, col]
    except:
        print("invalid coordinate")


# def compute_black_vc(stone: list):
#         """compute simple virutal connections for a black stone on the board"""
#         move = coord_to_move(stone)
#         row = move[0]
#         col = move[1]
#         vcs = []

#         # Check if the stone is in the top left corner of the board.
#         # If it is, that means it only has a bridge connection to the lower right cell.
#         if col == 0 and row == 0:
#             lower_right_vc = [row + 1, col]
#             vcs.append(lower_right_vc)
        
#         # Check if the stone is in the bottom right corner of the board. 
#         # If it is, that means it only has a bridge connection to the upper left cell.
#         elif col == (size - 1) and row == (size - 1):
#             upper_left_vc = [row - 1, col]
#             vcs.append(upper_left_vc)
        
#         # Check if the stone is in the first row of the board, but not the first left corner.
#         # If it is, that means it only has a bridge connection to the lower left/right cells.
#         elif row == 0 and row != col:
#             lower_left_vc = [row + 1, col - 1]
#             lower_right_vc = [row + 1, col]
#             vcs.append(lower_left_vc)
#             vcs.append(lower_right_vc)

#         # Check if the stone is in the last row of the board, but not the last right corner.
#         # If it is, that means it only has a bridge connection to the upper left/right cells.
#         elif row == (size - 1) and row != col:
#             upper_left_vc = [row - 1, col]
#             upper_right_vc = [row - 1, col + 1]
#             vcs.append(upper_left_vc)
#             vcs.append(upper_right_vc)
        
#         # Check if the stone is in the leftmost edge of the board but not the top/bottom left corner.
#         # If it is, it will be missing a lower left bridge connection.
#         elif col == 0 and row != col and row != (size - 1):
#             upper_left_vc = [row - 1, col]
#             upper_right_vc = [row - 1, col + 1]
#             lower_right_vc = [row + 1, col]
#             vcs.append(upper_left_vc)
#             vcs.append(upper_right_vc)
#             vcs.append(lower_right_vc)
        
#         # Check if the stone is in the rightmost edge of the board but not the top/bottom right corner.
#         # If it is, it will be missing an upper right bridge connection.
#         elif col == (size - 1) and row != 0 and row != col:
#             upper_left_vc = [row - 1, col]
#             lower_left_vc = [row + 1, col - 1]
#             lower_right_vc = [row + 1, col]
#             vcs.append(upper_left_vc)
#             vcs.append(lower_left_vc)
#             vcs.append(lower_right_vc)

#         # The stone is not in the edges of the board.
#         # This means it has a bridge connection to all combinations of upper/lower/left/right cells.
#         else:
#             upper_left_vc = [row - 1, col]
#             upper_right_vc = [row - 1, col + 1]
#             lower_left_vc = [row + 1, col - 1]
#             lower_right_vc = [row + 1, col]
#             vcs.append(upper_left_vc)
#             vcs.append(upper_right_vc)
#             vcs.append(lower_left_vc)
#             vcs.append(lower_right_vc)

#         # Return the final list of virtual connections.
#         return vcs


def command_loop(game):
    command = None
    while command != "exit" and command != "quit" and command != "q":
        print("= ", end="")
        command = input().lower()
        
        if command == "":
            continue

        args = command.split()
        try:
            if args[0] == "x":
                previous_game = game.copy()
                move = coord_to_move(args[1])
                game.play_move(move, BLACK)
                print(str(game))
            elif args[0] == "o":
                previous_game = game.copy()
                move = coord_to_move(args[1])
                game.play_move(move, WHITE)
                print(str(game))
            elif args[0] == ".":
                previous_game = game.copy()
                move = coord_to_move(args[1])
                game.clear_move(move)
                print(str(game))
            elif args[0] == "show":
                print(str(game))
            elif args[0] == "size":
                global size
                size = int(args[1])
                if version == "0":
                    game = hex_game0.Hex(size)
                elif version == "1.0" or version == "1":
                    game = hex_game1.Hex1(size)
                elif version == "1.1":
                    game = hex_game1_1.Hex1_1(size)
                elif version == "2":
                    game = hex_game2.Hex2(size)
            elif args[0] == "reset":
                previous_game = game.copy()
                if version == "0":
                    game = hex_game0.Hex(size)
                elif version == "1.0" or version == "1":
                    game = hex_game1.Hex1(size)
                elif version == "1.1":
                    game = hex_game1_1.Hex1_1(size)
                elif version == "2":
                    game = hex_game2.Hex2(size)
            elif args[0] == "undo":
                game = previous_game
                print(str(game))
            elif args[0] == "version":
                pass
            elif args[0] == "mcts":
                if args[1] == "x":
                    previous_game = game.copy()
                    mcts = mcts1.Mcts(game, BLACK)
                    move = mcts.monte_carlo_tree_search()
                    #cProfile.runctx('mcts.monte_carlo_tree_search()', globals(), locals())
                    #exit()
                    print("number of simulations performed:", mcts.root_node.sims)
                    game.play_move(move, BLACK)
                    print(str(game))
                elif args[1] == "o":
                    previous_game = game.copy()
                    mcts = mcts1.Mcts(game, WHITE)
                    move = mcts.monte_carlo_tree_search()
                    print("number of simulations performed:", mcts.root_node.sims)
                    game.play_move(move, WHITE)
                    print(str(game))
            elif args[0] == "pns":
                if args[1] == "x":
                    pns = pns0.PNS(game, BLACK)
                    pns.pns()
            elif args[0] == "bvc":
                mutual_vc = game.check_black_vcs(coord_to_move(args[1]), coord_to_move(args[2]))
                print(str(game))
                print("The mutual VCs between", args[1], "and", args[2], "is:", mutual_vc)
        except IndexError:
            continue


if __name__=="__main__":
    print("version: ", version)
    if version == "0":
        game = hex_game0.Hex(size)
    elif version == "1.0" or version == "1":
        game = hex_game1.Hex1(size)
    elif version == "1.1":
        game = hex_game1_1.Hex1_1(size)
    elif version == "2":
        game = hex_game2.Hex2(size)
    command_loop(game)
