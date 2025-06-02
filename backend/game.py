import copy
import random
from MCTSStrategy import MCTSNode, MCTSStrategy


class Game:
    def __init__(self):
        self.reset()
        self._state_stack = []

    def reset(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.board_wins = [0] * 9
        self.turn = 1
        self.cur_move_type = 0
        self.winner = 0
        self._state_stack = []

    def make_move(self, move_id):
        mini_board = (move_id - 1) // 9
        mini_loc = (move_id - 1) % 9

        if (
            self.board[mini_board][mini_loc] == 0
            and (self.cur_move_type == 0 or self.cur_move_type == mini_board + 1)
            and self.board_wins[mini_board] == 0
        ):
            self.board[mini_board][mini_loc] = self.turn

            if self.is_winner(self.board[mini_board], self.turn):
                self.board_wins[mini_board] = self.turn

            if self.board_wins[mini_loc] == 0 and any(
                self.board[mini_loc][i] == 0 for i in range(9)
            ):
                self.cur_move_type = mini_loc + 1
            else:
                self.cur_move_type = 0

            self.turn = 3 - self.turn

    def is_winner(self, board, player):
        win_indices = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        return any(all(board[i] == player for i in indices) for indices in win_indices)

    def check_winner(self):
        if not self.get_valid_moves():
            return 3
        if self.is_winner(self.board_wins, 1):
            return 1
        if self.is_winner(self.board_wins, 2):
            return 2
        return 0

    def get_valid_moves(self):
        valid = []
        for mini in range(9):
            if self.board_wins[mini] != 0:
                continue
            if self.cur_move_type and self.cur_move_type != mini + 1:
                continue
            for i in range(9):
                if self.board[mini][i] == 0:
                    valid.append(mini * 9 + i + 1)
        return valid

    def evaluate_one(self, player):
        winner = self.check_winner()
        if winner == player:
            return 100
        elif winner and winner != player:
            return -100
        return sum(10 if w == player else -10 if w != 0 else 0 for w in self.board_wins)

    def evaluate_two(self, player):
        winner = self.check_winner()
        if winner == player:
            return 100
        elif winner and winner != player:
            return -100

        opponent = 3 - player
        score = 0

        for mini in range(9):
            mini_board = self.board[mini]
            w = self.board_wins[mini]
            if w == player:
                score += 20
            elif w == opponent:
                score -= 20
            else:
                for indices in self._win_indices():
                    line = [mini_board[i] for i in indices]
                    if line.count(player) == 2 and line.count(0) == 1:
                        score += 3
                    if line.count(opponent) == 2 and line.count(0) == 1:
                        score -= 3

        for indices in self._win_indices():
            line = [self.board_wins[i] for i in indices]
            if line.count(player) == 2 and line.count(0) == 1:
                score += 15
            if line.count(opponent) == 2 and line.count(0) == 1:
                score -= 15

        return score

    def _win_indices(self):
        return [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]

    def order_moves(self, moves):
        def score(move):
            loc = (move - 1) % 9
            return 3 if loc == 4 else 2 if loc in [0, 2, 6, 8] else 1

        return sorted(moves, key=score, reverse=True)

    def _save_state(self):
        self._state_stack.append(
            (
                copy.deepcopy(self.board),
                self.board_wins[:],
                self.turn,
                self.cur_move_type,
            )
        )

    def _restore_state(self):
        self.board, self.board_wins, self.turn, self.cur_move_type = (
            self._state_stack.pop()
        )

    def dlminimax(self, depth, alpha, beta, maximizing, player, eval_func):
        winner = self.check_winner()
        if winner != 0 or depth == 0:
            return eval_func(player)

        valid_moves = self.order_moves(self.get_valid_moves())

        if maximizing:
            max_eval = -float("inf")
            for move in valid_moves:
                self._save_state()
                self.make_move(move)
                eval = self.dlminimax(depth - 1, alpha, beta, False, player, eval_func)
                self._restore_state()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in valid_moves:
                self._save_state()
                self.make_move(move)
                eval = self.dlminimax(depth - 1, alpha, beta, True, player, eval_func)
                self._restore_state()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self, depth, eval_func):
        valid_moves = self.get_valid_moves()
        best_val = -float("inf")
        best_move = None
        player = self.turn

        for move in valid_moves:
            self._save_state()
            self.make_move(move)
            eval = self.dlminimax(
                depth,
                -float("inf"),
                float("inf"),
                False,
                player,
                eval_func,
            )
            self._restore_state()
            if eval > best_val:
                best_val = eval
                best_move = move
        if best_move:
            self.make_move(best_move)
        return best_move

    def best_mcts_move(self, iterations=1000):
        mcts = MCTSStrategy(iterations=iterations)
        best_move = mcts(self)
        return best_move

    def find_best_mcts_move(self, iterations=1000):
        mcts = MCTSStrategy(iterations=iterations)
        root = self.get_root(self, iterations)
        best_move = max(root.children, key=lambda c: c.visits).move
        return best_move

    def get_root(self, game, iterations):
        player = game.turn
        root = MCTSNode(game)
        for _ in range(iterations):
            node = root
            while node.children and node.is_fully_expanded():
                node = node.best_child()
            if node.visits == 0:
                node.expand()
            if node.children:
                node = random.choice(node.children)
            result = node.simulate()
            node.backpropagate(result, player)
        return root

    def find_best_move(self, depth, eval_func):
        valid_moves = self.get_valid_moves()
        best_val = -float("inf")
        best_move = None
        player = self.turn

        for move in valid_moves:
            self._save_state()
            self.make_move(move)
            eval = self.dlminimax(
                depth,
                -float("inf"),
                float("inf"),
                False,
                player,
                eval_func,
            )
            self._restore_state()
            if eval > best_val:
                best_val = eval
                best_move = move
        return best_move
