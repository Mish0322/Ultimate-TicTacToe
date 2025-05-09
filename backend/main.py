import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import  CORSMiddleware
from pydantic import BaseModel
from game import Game


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

app = FastAPI()

origins = [
    "https://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],)

gamestate = Game()

@app.get("/", response_model=Board)
def get_board():
    return Board(board=gamestate.board, cur_move_type=gamestate.cur_move_type)

@app.post("/move", response_model=Board)
def make_move(move: Move):
    gamestate.make_move(move.square)
    return Board(board=gamestate.board, cur_move_type=gamestate.cur_move_type)

@app.delete("/reset", response_model=Board)
def reset():
    gamestate = Game()
    return Board(board=gamestate.board, cur_move_type=gamestate.cur_move_type)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
