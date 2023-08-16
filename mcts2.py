# Monte Carlo Tree Search implementation based off of Ryan Hayward's
# pseudocode from https://webdocs.cs.ualberta.ca/~hayward/355/jem/mcts.html
# Accessed August 16, 2023
#
# Written with the help of GitHub Copilot

import time
import copy
import random

TURNTIME = 15  # measured in seconds

class Node:
    def __init__(self, move, parent, depth):
        # move is from parent to node
        self.move = move
        self.parent = parent
        self.children = []
        self.depth = depth
        
        self.wins = 0
        self.visits = 0

    def expand_node(self, state):
        if not state._check_win():
            for move in state.get_legal_moves():
                self.children.append(Node(move, self, self.depth + 1))

    def update(self, won):
        self.visits += 1
        if won:
            self.wins += 1

    def is_leaf(self):
        return len(self.children) == 0

    def has_parent(self):
        return self.parent is not None

class MCTS:
    def __init__(self):
        pass

    def mcts(self, state):
        root_node = Node(None, None, 0)
        
        end_time = time.time() + TURNTIME

        while time.time() < end_time:
            node = root_node
            state_copy = state.copy()
            while not node.is_leaf():
                node = self.tree_policy_child(node)
                # TODO: remove win check from play move
                state_copy.play_move(node.move)
            node.expand_node(state_copy)
            node = self.tree_policy_child(node)
            while not state_copy._check_win():
                state_copy.play_move(self.simulation_policy_child(state_copy))
            result = self.evaluate(state_copy, state.current_player)
            while node is not None and node.has_parent():
                node.update(result)
                node = node.parent
    
        return self.tree_policy_child(root_node).move

    def evaluate(self, state, original_player):
        assert(state._check_win())

        if state.current_player == original_player:
            return True

        return False

    def tree_policy_child(self, node):
        best_f = None
        best_child = None

        for child in random.sample(node.children, len(node.children)):
            f = (child.wins + 1) / (child.visits + 2)
            if node.depth % 2 == 0:  # at even depth, choose argmax
                if best_f == None or f > best_f:
                    best_f = f
                    best_child = child
            else:  # at odd depth, choose argmin
                if best_f == None or f < best_f:
                    best_f = f
                    best_child = child

        return best_child
    
    def simulation_policy_child(self, state):
        return random.choice(state.get_legal_moves())
