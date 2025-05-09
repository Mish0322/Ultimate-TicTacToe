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

    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.board_wins = [0] * 9
        self.turn = 1
        self.cur_move_type = 0

    def make_move(self, move_id):
        mini_board = (move_id - 1) // 9
        mini_board_loc = (move_id - 1) % 9

        # check valid move
        if self.board[mini_board][mini_board_loc] == 0 and (self.cur_move_type == 0 or self.cur_move_type == mini_board + 1) and self.board_wins[mini_board] == 0:

            # add it to board
            self.board[mini_board][mini_board_loc] = self.turn 

            # check for a mini_board win
            flag = False
            for index_set in [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:
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