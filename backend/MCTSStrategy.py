import copy
import math
import random


class MCTSNode:
    def __init__(self, game, move=None, parent=None):
        self.game = copy.deepcopy(game)
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def expand(self):
        if not self.children:
            valid_moves = self.game.get_valid_moves()
            for move in valid_moves:
                new_game = copy.deepcopy(self.game)
                new_game.make_move(move)
                self.children.append(MCTSNode(new_game, move, parent=self))

    def is_fully_expanded(self):
        return len(self.children) == len(self.game.get_valid_moves())

    def best_child(self, c=1.41):
        # UCB1
        def ucb1(child):
            if child.visits == 0:
                return float("inf")
            return (child.wins / child.visits) + c * math.sqrt(
                math.log(self.visits) / child.visits
            )

        return max(self.children, key=ucb1)

    def simulate(self):
        simulation_game = copy.deepcopy(self.game)
        while simulation_game.check_winner() == 0:
            valid_moves = simulation_game.get_valid_moves()
            move = random.choice(valid_moves)
            simulation_game.make_move(move)
        winner = simulation_game.check_winner()
        return winner

    def backpropagate(self, result, player):
        self.visits += 1
        if result == player:
            self.wins += 1
        elif result == 3:
            self.wins += 0.5
        if self.parent:
            self.parent.backpropagate(result, player)


class MCTSStrategy:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def __call__(self, game):
        player = game.turn 
        root = MCTSNode(game)

        for _ in range(self.iterations):
            node = root
            # Selection
            while node.children and node.is_fully_expanded():
                node = node.best_child()
            # Expansion
            if node.visits == 0:
                node.expand()
            if node.children:
                node = random.choice(node.children)
            # Simulation
            result = node.simulate()
            # Backpropagation
            node.backpropagate(result, player)
        if not root.children:
            return None
        best_move = max(root.children, key=lambda c: c.visits).move
        game.make_move(best_move)
        return best_move
