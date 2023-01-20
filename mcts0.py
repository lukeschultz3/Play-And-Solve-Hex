import time, random
from math import sqrt, log

import hex_game
from hex_game import ( BLACK, WHITE )

class TreeNode:
    def __init__(self, game: hex_game.Hex, color, move=None, parent=None):
        self.color = color    # player who needs to make move
        self.game = game      # hex_game Hex object
        self.move = move      # previous move
        self.parent = parent  # parent node, None if root

        self.wins = 0  # number of winning simulations
        self.sims = 0  # number of simulations

        self.generated_children = False  # true if node has been expanded
        self.children = []               # list of child nodes

        # legal moves from this position
        self.moves = self.game.get_legal_moves()

    def generate_children(self):
        """ function to generate children of this mode """
        for move in self.moves:
            game_copy = self.game.copy()
            game_copy.play_move(move, self.color)
            self.children.append(TreeNode(game_copy, -1*self.color, move, self))

        self.generated_children = True

    def rollout(self) -> bool:
        """ recursive function to run a simulation
        selects moves uniformly random """

        if len(self.moves) == 0:
            # color player lost
            return False

        game_copy = self.game.copy()
        color = self.color
        moves = game_copy.get_legal_moves()
        while len(moves) > 0:
            move_index = random.randint(0, len(moves)-1)  # select random move
            won = game_copy.play_move(moves[move_index], color)

            if won:
                break

            moves[move_index] = moves[-1]
            moves.pop()
            color *= -1  # invert color

        if color != self.color:
            # color player won
            return True
        else:
            # color player lost
            return False


class RootNode(TreeNode):
    def generate_children(self):
        """ function to generate children of this mode 
        returns winning move, if one is found """
        for move in self.moves:
            game_copy = self.game.copy()
            won = game_copy.play_move(move, self.color)
            if won:
                return move
            self.children.append(TreeNode(game_copy, -1*self.color, move, self))

        self.generated_children = True
        return None


class Mcts:
    # MCTS code largely taken from
    # https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
    # November 27, 2022

    def __init__(self, board, color):
        self.root_node = RootNode(board, color)
        self.winning_move = self.root_node.generate_children()

        self.c = 0.4  # used for UCT

    def get_best_move(self):
        """ function to get best move, based on amount of times
        it was chosen for simulation

        Returns:
            best move
        """
        best_node = None
        most_visits = None
        for node in self.root_node.children:
            if most_visits == None or node.sims > most_visits:
                best_node = node
                most_visits = node.sims

        return best_node.move

    def monte_carlo_tree_search(self):
        """ function that runs monte carlo tree search

        Returns:
            best_move: most visited move
        """

        if self.winning_move != None:
            print("number of simulations performed:", self.root_node.sims)
            return self.winning_move

        # return move after set amount of time
        end_time = time.time() + 15

        while time.time() < end_time:
            leaf = self.traverse(self.root_node)  # traverse
            won = leaf.rollout()  # rollout

            # backpropagate
            node = leaf
            while node != None: 
                node.sims += 1

                if won and node.color == leaf.color:
                    node.wins += 1
                elif not won and node.color != leaf.color:
                    node.wins += 1

                node = node.parent

        print("number of simulations performed:", self.root_node.sims)
        return self.get_best_move()

    def best_uct(self, node: TreeNode) -> TreeNode:
        """ function that finds next move for traversal,
        if node is a root, will return node
        if there is at least one child of node that has not been simulated on,
            will return that child
        otherwise, will return child with best uct score

        Arguments:
            node: node in tree to find child to traverse for

        Returns:
            next node to traverse
        """

        if len(node.moves) == 0:
            return node  # if terminal node, return node

        best_uct = None
        best_child = None

        for child in node.children:
            if child.sims == 0:
                # if the children of the node have not been
                # fully explored, then explore a move that
                # hasn't been before
                return child

            # calculate UCT, update if best
            mean_wins = child.wins / child.sims
            uct = mean_wins+(self.c*sqrt(log(self.root_node.sims)/child.sims))
            if best_uct == None or uct > best_uct:
                best_uct = uct
                best_child = child

        # return best uct
        return best_child

    def traverse(self, node: TreeNode):
        """ function that traverses tree and finds node to simulate

        Arguments:
            node: root (first move) of tree

        Returns:
            node: move to run simulation on
            visited: list of nodes visited, needed for backprop
        """
        while node.generated_children:
            node = self.best_uct(node)

        if len(node.moves) > 0 and node.sims > 0:
            node.generate_children()
            node = random.choice(node.children)

        return node
