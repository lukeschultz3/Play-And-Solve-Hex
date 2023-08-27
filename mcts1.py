# Created by Luke Schultz
# Fall 2022, Winter 2023


import time
import random
from math import sqrt, log


class TreeNode:
    def __init__(self, game, player: int, move=None, parent=None):
        self.game = game      # Hex object
        self.player = player  # Player to make move
        self.move = move      # Previous move
        self.parent = parent  # Parent node, None if root

        self.results = 0  # +1 for black win, -1 for white win
        self.sims = 0  # Number of simulations

        self.generated_children = False  # True if node has been expanded
        self.children = []               # List of child nodes

        # Legal moves from this position
        self.moves = self.game.get_legal_moves()

    def generate_children(self):
        """Generate children of this mode."""

        for move in self.moves:
            game_copy = self.game.copy()
            won = game_copy.play_move(move, self.player)
            self.children.append(
                TreeNode(game_copy, 3-self.player, move, self)
            )

            if won:
                # backpropagate
                node = self.children[-1]
                result = float('inf')
                while node is not None:
                    if result == float('inf') and node != self.children[-1]:
                        for children in node.children:
                            if children.results != float('-inf'):
                                result = 1
                                break

                    node.results += result

                    if result == float('inf'):
                        result = float('-inf')
                    elif result == float('-inf'):
                        result = float('inf')
                    else:
                        result = 1-result

                    node = node.parent

        self.generated_children = True

    def rollout(self) -> bool:
        """
        Perform a simulation.
        Selects moves uniformly random.

        Returns:
        bool: True if self.player won
        """

        game_copy = self.game.copy()
        player = self.player  # player to move
        moves = game_copy.get_legal_moves()
        while len(moves) > 0:
            move_index = random.randint(0, len(moves)-1)  # Select random move
            won = game_copy.play_move(moves[move_index], player)

            if won:
                break

            moves[move_index] = moves[-1]
            moves.pop()
            player = 3 - player  # invert color / switch player

        if player != self.player:  # self.player won
            return 1
        else:  # self.player lost
            return 0


class RootNode(TreeNode):
    def generate_children(self):
        """
        Generate children of this node.

        Returns:
        winning move, if one is found
        """

        for move in self.moves:
            game_copy = self.game.copy()
            won = game_copy.play_move(move, self.player)

            if won:
                return move

            self.children.append(
                TreeNode(game_copy, 3-self.player, move, self)
            )

        self.generated_children = True
        return None


class Mcts:
    # MCTS code largely taken from
    # https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
    # November 27, 2022

    def __init__(self, game, player):
        self.root_node = RootNode(game, player)
        self.winning_move = self.root_node.generate_children()

        self.c = 0.3  # used for UCT

    def get_best_move(self):
        """
        Get most simulated move.

        Returns:
        move: most simulated move
        """

        best_node = None
        most_visits = None
        for node in self.root_node.children:
            if node.results == float('-inf'):
                continue

            if most_visits is None or node.sims > most_visits:
                best_node = node
                most_visits = node.sims

        if best_node is None: 
            # all moves are losing, choose the one with the most visits
            for node in self.root_node.children:
                if most_visits is None or node.sims > most_visits:
                    best_node = node
                    most_visits = node.sims

        return best_node.move

    def monte_carlo_tree_search(self):
        """
        Perform Monte Carlo Tree Search.

        Returns:
            best_move: most visited move
        """

        if self.winning_move is not None:
            print("number of simulations performed:", self.root_node.sims)
            return self.winning_move

        # return move after set amount of time
        end_time = time.time() + 15

        while time.time() < end_time:
            leaf = self.traverse(self.root_node)  # traverse
            result = leaf.rollout()  # rollout

            # backpropagate
            node = leaf
            while node is not None:
                node.sims += 1

                if result == float('inf') and node != leaf:
                    for children in node.children:
                        if children.results != float('-inf'):
                            result = 1
                            break
                elif result == float('inf') and node.parent is None:
                    return node.move

                node.results += result

                #result *= -1
                if result == float('inf'):
                    result = float('-inf')
                elif result == float('-inf'):
                    result = float('inf')
                else:
                    result = 1-result

                node = node.parent

        for child in self.root_node.children:
            print(child.move, child.sims, child.results)
        return self.get_best_move()

    def best_uct(self, node: TreeNode) -> TreeNode:
        """
        Return the next move for traversal.

        If node is a root, return node.
        If there is a child of node that has not been simulated, return child.
        Otherwise, return child with best uct score.

        Arguments:
        node (TreeNode): Node in tree to find child to traverse for

        Returns:
        TreeNode: child to traverse
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
            mean_result = child.results / child.sims
            uct = mean_result+(self.c*sqrt(log(self.root_node.sims)/child.sims))
            if best_uct is None or uct > best_uct:
                best_uct = uct
                best_child = child

        # return best uct
        return best_child

    def traverse(self, node: TreeNode):
        """
        Traverse tree and find node to simulate.

        Arguments:
        node (TreeNode): Root (first move) of tree

        Returns:
        Node (TreeNode): move to run simulation on
        """

        while node.generated_children:
            node = self.best_uct(node)

        if len(node.moves) > 0 and node.sims > 0:
            node.generate_children()
            node = random.choice(node.children)

        return node