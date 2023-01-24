import hex_game
import hex_game1
from hex_game import BLACK, WHITE, BLANK
import mcts0

import cProfile

size = 3
previous_game = None

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
                game = hex_game.Hex(size)
            elif args[0] == "reset":
                previous_game = game.copy()
                game = hex_game.Hex(size)
            elif args[0] == "undo":
                game = previous_game
                print(str(game))
            elif args[0] == "mcts":
                if args[1] == "x":
                    previous_game = game.copy()
                    mcts = mcts0.Mcts(game, BLACK)
                    move = mcts.monte_carlo_tree_search()
                    #cProfile.runctx('mcts.monte_carlo_tree_search()', globals(), locals())
                    #exit()
                    game.play_move(move, BLACK)
                    print(str(game))
                elif args[1] == "o":
                    previous_game = game.copy()
                    mcts = mcts0.Mcts(game, WHITE)
                    move = mcts.monte_carlo_tree_search()
                    game.play_move(move, WHITE)
                    print(str(game))
        except IndexError:
            continue


if __name__=="__main__":
    game = hex_game1.Hex(size)
    command_loop(game)
