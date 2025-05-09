import React from "react";
import MiniBoard from "./MiniBoard"

function Board({board, click, cur_move_type, board_wins}) {
    let highlight = new Array(9).fill(cur_move_type === 0 ? 3 : 0);
    if (cur_move_type !== 0) {
        highlight[cur_move_type - 1] = 3
    }

    for(let i = 0; i < 9; i++){
        if (board_wins[i] !== 0) {
            highlight[i] = board_wins[i]
        }
    }

    return (
        <div className="board">
            <MiniBoard board={board[0]} id={0} click={click} highlight={highlight[0]}/>
            <MiniBoard board={board[1]} id={1} click={click} highlight={highlight[1]}/>
            <MiniBoard board={board[2]} id={2} click={click} highlight={highlight[2]}/>
            <MiniBoard board={board[3]} id={3} click={click} highlight={highlight[3]}/>
            <MiniBoard board={board[4]} id={4} click={click} highlight={highlight[4]}/>
            <MiniBoard board={board[5]} id={5} click={click} highlight={highlight[5]}/>
            <MiniBoard board={board[6]} id={6} click={click} highlight={highlight[6]}/>
            <MiniBoard board={board[7]} id={7} click={click} highlight={highlight[7]}/>
            <MiniBoard board={board[8]} id={8} click={click} highlight={highlight[8]}/>
        </div>
    )
}

export default Board;