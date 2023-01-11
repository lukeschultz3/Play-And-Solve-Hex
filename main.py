import hex_game
from hex_game import BLACK, WHITE, BLANK
from mcts import Mcts

size = 3
previous_game = None

def command_loop(game):
    command = None
    while command != "exit" and command != "quit":
        print("= ", end="")
        command = input().lower()
        
        if command == "":
            continue

        args = command.split()
        try:
            if args[0] == "x":
                previous_game = game.copy()
                game.play_move([int(args[1]), int(args[2])], BLACK)
                print(str(game))
            elif args[0] == "o":
                previous_game = game.copy()
                game.play_move([int(args[1]), int(args[2])], WHITE)
                print(str(game))
            elif args[0] == ".":
                previous_game = game.copy()
                game.clear_move([int(args[1]), int(args[2])])
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
                    mcts = Mcts(game, BLACK)
                    move = mcts.monte_carlo_tree_search()
                    game.play_move(move, BLACK)
                    print(str(game))
                elif args[1] == "o":
                    previous_game = game.copy()
                    mcts = Mcts(game, WHITE)
                    move = mcts.monte_carlo_tree_search()
                    game.play_move(move, WHITE)
                    print(str(game))
        except IndexError:
            continue


if __name__=="__main__":
    game = hex_game.Hex(size)
    command_loop(game)