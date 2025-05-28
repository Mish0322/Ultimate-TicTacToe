class Game:
    # 9 by 9 list to simulate the board
    # 0 for open-space, 1 for P1, 2 for P2
    # outer lists are by mini tic-tac-toe boards
    board: list[list[int]]

    # 1 for P1, 2 for P2
    turn: int

    # 0 for anymove, 1-9 for different mini tic-tac-toes
    cur_move_type: int

    # 1 for P1, 2 for P2, keeps track of all the mini-board wins
    board_wins: list[int]

    winner: int

    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.board_wins = [0] * 9
        self.turn = 1
        self.cur_move_type = 0
        self.winner = 0

    def make_move(self, move_id):
        mini_board = (move_id - 1) // 9
        mini_board_loc = (move_id - 1) % 9

        # check valid move
        if (
            self.board[mini_board][mini_board_loc] == 0
            and (self.cur_move_type == 0 or self.cur_move_type == mini_board + 1)
            and self.board_wins[mini_board] == 0
        ):

            # add it to board
            self.board[mini_board][mini_board_loc] = self.turn

            # check for a mini_board win
            flag = False
            for index_set in [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [1, 4, 7],
                [2, 5, 8],
                [3, 6, 9],
                [1, 5, 9],
                [3, 5, 7],
            ]:
                temp = True
                for index in index_set:
                    if self.board[mini_board][index - 1] != self.turn:
                        temp = False

                if temp:
                    flag = True
                    break

            if flag:
                self.board_wins[mini_board] = self.turn

            # create next move_type
            if self.board_wins[mini_board_loc] == 0:
                flag = True
                for index in range(9):
                    if self.board[mini_board_loc][index] == 0:
                        flag = False
                        break

                self.cur_move_type = 0 if flag else mini_board_loc + 1

            else:
                self.cur_move_type = 0

            # update turn
            self.turn = 1 if self.turn == 2 else 2

    def reset(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.board_wins = [0] * 9
        self.turn = 1
        self.cur_move_type = 0
        self.winner = 0

    def check_winner(self):
        if len(self.get_valid_moves()) == 0:
            return 3
            # tie
        for index_set in [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7],
        ]:
            if all(self.board_wins[index - 1] == 1 for index in index_set):
                return 1  # P1 wins
            if all(self.board_wins[index - 1] == 2 for index in index_set):
                return 2  # P2 wins
        return 0  # No winner yet

    def get_valid_moves(self):
        valid_moves = []
        for mini_board in range(9):
            # Skip if this mini-board is already won
            if self.board_wins[mini_board] != 0:
                continue
            # Skip if we must play a specific mini-board
            if self.cur_move_type != 0 and self.cur_move_type != mini_board + 1:
                continue
            # Check for empty tiles
            for index in range(9):
                if self.board[mini_board][index] == 0:
                    move_id = mini_board * 9 + index + 1
                    valid_moves.append(move_id)
        return valid_moves

    def minimax(self, alpha, beta, maximizing_player, player):
        winner = self.check_winner()
        if winner == player:
            return 1
        elif winner != 0 and winner != player:
            return -1
        elif winner == 3:  # Tie
            return 0

        valid_moves = self.get_valid_moves()

        if maximizing_player:
            max_eval = -float("inf")
            for move in valid_moves:
                # Save current state
                prev_board = [row[:] for row in self.board]
                prev_board_wins = self.board_wins[:]
                prev_turn = self.turn
                prev_cur_move_type = self.cur_move_type

                self.make_move(move)
                eval = self.minimax(alpha, beta, False, player)
                # Undo move
                self.board = prev_board
                self.board_wins = prev_board_wins
                self.turn = prev_turn
                self.cur_move_type = prev_cur_move_type

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in valid_moves:
                # Save current state
                prev_board = [row[:] for row in self.board]
                prev_board_wins = self.board_wins[:]
                prev_turn = self.turn
                prev_cur_move_type = self.cur_move_type

                self.make_move(move)
                eval = self.minimax(alpha, beta, True, player)
                # Undo move
                self.board = prev_board
                self.board_wins = prev_board_wins
                self.turn = prev_turn
                self.cur_move_type = prev_cur_move_type

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_move_full_search(self):
        valid_moves = self.get_valid_moves()
        best_val = -float("inf")
        best_move = None
        player = self.turn
        n = 0

        for move in valid_moves:
            # Save current state
            print(n)
            n += 1
            prev_board = [row[:] for row in self.board]
            prev_board_wins = self.board_wins[:]
            prev_turn = self.turn
            prev_cur_move_type = self.cur_move_type

            self.make_move(move)
            eval = self.minimax(-float("inf"), float("inf"), False, player)
            # Undo move
            self.board = prev_board
            self.board_wins = prev_board_wins
            self.turn = prev_turn
            self.cur_move_type = prev_cur_move_type

            if eval > best_val:
                best_val = eval
                best_move = move

        return best_move

    def evaluate(self, player):
        # If game over
        winner = self.check_winner()
        if winner == player:
            return 100
        elif winner != 0 and winner != player:
            return -100

        # Otherwise, heuristic: mini-board wins
        score = 0
        for w in self.board_wins:
            if w == player:
                score += 10
            elif w != 0 and w != player:
                score -= 10
        return score

    def dlminimax(self, depth, alpha, beta, maximizing_player, player):
        winner = self.check_winner()
        if winner != 0 or depth == 0:
            return self.evaluate(player)

        valid_moves = self.get_valid_moves()

        if maximizing_player:
            max_eval = -float("inf")
            for move in valid_moves:
                # Save full state
                prev_board = [row[:] for row in self.board]
                prev_board_wins = self.board_wins[:]
                prev_turn = self.turn
                prev_cur_move_type = self.cur_move_type

                # Make the move
                self.make_move(move)
                eval = self.dlminimax(depth - 1, alpha, beta, False, player)

                # Undo fully
                self.board = prev_board
                self.board_wins = prev_board_wins
                self.turn = prev_turn
                self.cur_move_type = prev_cur_move_type

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in valid_moves:
                # Save full state
                prev_board = [row[:] for row in self.board]
                prev_board_wins = self.board_wins[:]
                prev_turn = self.turn
                prev_cur_move_type = self.cur_move_type

                self.make_move(move)
                eval = self.dlminimax(depth - 1, alpha, beta, True, player)

                # Undo fully
                self.board = prev_board
                self.board_wins = prev_board_wins
                self.turn = prev_turn
                self.cur_move_type = prev_cur_move_type

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self):
        valid_moves = self.get_valid_moves()
        best_val = -float("inf")
        best_move = None
        player = self.turn
        n = 0

        for move in valid_moves:
            print(f"Testing move number: {n}", end="\r")
            n += 1
            # Save current state
            prev_board = [row[:] for row in self.board]
            prev_board_wins = self.board_wins[:]
            prev_turn = self.turn
            prev_cur_move_type = self.cur_move_type

            # Try the move
            self.make_move(move)
            eval = self.dlminimax(7, -float("inf"), float("inf"), False, player)

            # Undo move
            self.board = prev_board
            self.board_wins = prev_board_wins
            self.turn = prev_turn
            self.cur_move_type = prev_cur_move_type

            if eval > best_val:
                best_val = eval
                best_move = move

        # Actually make the best move
        if best_move:
            self.make_move(best_move)

        return best_move
