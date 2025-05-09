import React from "react";
import MiniBoard from "./MiniBoard"

function Board({board, click}) {
    return (
        <div className="board">
            <MiniBoard board={board[0]} id={0} click={click} />
            <MiniBoard board={board[1]} id={1} click={click} />
            <MiniBoard board={board[2]} id={2} click={click} />
            <MiniBoard board={board[3]} id={3} click={click} />
            <MiniBoard board={board[4]} id={4} click={click} />
            <MiniBoard board={board[5]} id={5} click={click} />
            <MiniBoard board={board[6]} id={6} click={click} />
            <MiniBoard board={board[7]} id={7} click={click} />
            <MiniBoard board={board[8]} id={8} click={click} />
        </div>
    )
}

export default Board;