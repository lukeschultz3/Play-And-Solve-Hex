import hex_game
from hex_game import BLACK, WHITE
from mcts import Mcts

def command_loop(game):
    command = None
    while command != "exit" and command != "quit":
        print("= ", end="")
        command = input().lower()
        
        if command == "":
            continue

        args = command.split()
        if args[0] == "x":
            game.play_move([int(args[1]), int(args[2])], BLACK)
        elif args[0] == "o":
            game.play_move([int(args[1]), int(args[2])], WHITE)
        elif args[0] == "show":
            print(str(game))
        elif args[0] == "mcts":
            if args[1] == "x":
                mcts = Mcts(game, BLACK)
                move = mcts.monte_carlo_tree_search()
                game.play_move(move, BLACK)
            elif args[1] == "o":
                mcts = Mcts(game, WHITE)
                move = mcts.monte_carlo_tree_search()
                game.play_move(move, WHITE)


if __name__=="__main__":
    game = hex_game.Hex(5)
    command_loop(game)
