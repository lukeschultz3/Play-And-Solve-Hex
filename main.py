import hex_game0
import hex_game1
import hex_game1_1
from hex_game0 import BLACK, WHITE, BLANK
import mcts0

import cProfile

size = 8
previous_game = None
version = "0"  # "0" or "1" or "1.1"

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
                elif version == "1.0" or "1":
                    game = hex_game1.Hex(size)
                elif version == "1.1":
                    game = hex_game1_1.Hex1_1(size)
            elif args[0] == "reset":
                previous_game = game.copy()
                if version == "0":
                    game = hex_game0.Hex(size)
                elif version == "1.0" or "1":
                    game = hex_game1.Hex(size)
                elif version == "1.1":
                    game = hex_game1_1.Hex1_1(size)
            elif args[0] == "undo":
                game = previous_game
                print(str(game))
            elif args[0] == "version":
                pass
            elif args[0] == "mcts":
                if args[1] == "x":
                    previous_game = game.copy()
                    mcts = mcts0.Mcts(game, BLACK)
                    move = mcts.monte_carlo_tree_search()
                    print("number of simulations performed:", mcts.root_node.sims)
                    game.play_move(move, BLACK)
                    print(str(game))
                elif args[1] == "o":
                    previous_game = game.copy()
                    mcts = mcts0.Mcts(game, WHITE)
                    move = mcts.monte_carlo_tree_search()
                    print("number of simulations performed:", mcts.root_node.sims)
                    game.play_move(move, WHITE)
                    print(str(game))
        except IndexError:
            continue


if __name__=="__main__":
    if version == "0":
        game = hex_game0.Hex(size)
    elif version == "1.0" or "1":
        game = hex_game1.Hex(size)
    elif version == "1.1":
        game = hex_game1_1.Hex1_1(size)
    command_loop(game)
