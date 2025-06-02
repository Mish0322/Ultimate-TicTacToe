import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from game import Game
from random import choice
from MCTSStrategy import MCTSStrategy


class Move(BaseModel):
    # number 1 - 81 coresponding to square,
    # note that each mini-board has sets of 9
    # ex:
    # 1 2 3 10 11 12
    # 4 5 6 13 14 15
    # 7 8 9 16 17 18
    square: int


class Board(BaseModel):
    # 9 by 9 list to simulate the board
    # 0 for open-space, 1 for P1, 2 for P2
    board: list[list[int]]

    # 0 for anymove, 1-9 for different mini tic-tac-toes
    cur_move_type: int

    # 1 for P1, 2 for P2, keeps track of all the mini-board wins
    board_wins: list[int]
    winner: int


app = FastAPI()

origins = ["https://localhost:8000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

gamestate = Game()


@app.get("/", response_model=Board)
def get_board():
    return Board(
        board=gamestate.board,
        cur_move_type=gamestate.cur_move_type,
        board_wins=gamestate.board_wins,
    )


@app.post("/move", response_model=Board)
def make_move(move: Move):
    gamestate.make_move(move.square)
    winner = gamestate.check_winner()
    return {
        "board": gamestate.board,
        "cur_move_type": gamestate.cur_move_type,
        "board_wins": gamestate.board_wins,
        "winner": winner,
    }


@app.delete("/reset", response_model=Board)
def reset():
    gamestate.reset()
    return {
        "board": gamestate.board,
        "cur_move_type": gamestate.cur_move_type,
        "board_wins": gamestate.board_wins,
        "winner": 0,
    }


from random import choice


@app.post("/random_move", response_model=Board)
def random_move():
    valid_moves = gamestate.get_valid_moves()
    if valid_moves:
        move_id = choice(valid_moves)
        gamestate.make_move(move_id)
    winner = gamestate.check_winner()
    return {
        "board": gamestate.board,
        "cur_move_type": gamestate.cur_move_type,
        "board_wins": gamestate.board_wins,
        "winner": winner,
    }


@app.post("/best_move", response_model=Board)
def best_move():
    move = gamestate.best_move(depth=4)
    if move:
        gamestate.make_move(move)
    winner = gamestate.check_winner()
    print(gamestate.evaluateTwo(1))
    print(gamestate.evaluateOne(1))
    return {
        "board": gamestate.board,
        "cur_move_type": gamestate.cur_move_type,
        "board_wins": gamestate.board_wins,
        "winner": winner,
    }


def move_to_board_cell(move_id):
    mini_board = (move_id - 1) // 9 + 1
    cell = (move_id - 1) % 9 + 1
    return {"move": move_id, "mini_board": mini_board, "cell": cell}


@app.get("/suggest_moves")
def suggest_moves():
    suggestions = {}

    move1 = gamestate.find_best_move(depth=5, eval_func=gamestate.evaluate_one)
    move2 = gamestate.find_best_move(depth=5, eval_func=gamestate.evaluate_two)
    move3 = gamestate.find_best_mcts_move(iterations=1000)

    suggestions["minimax_one"] = move_to_board_cell(move1) if move1 else None
    suggestions["minimax_two"] = move_to_board_cell(move2) if move2 else None
    suggestions["mcts"] = move_to_board_cell(move3) if move3 else None

    return suggestions


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
