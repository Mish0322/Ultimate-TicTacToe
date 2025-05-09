import React from "react";
import Tile from "./Tile";

function MiniBoard({board, id, click}) {
    return (
        <div className="miniboard">
            <Tile state={board[0]} id={9*id+1} click={click} />
            <Tile state={board[1]} id={9*id+2} click={click} />
            <Tile state={board[2]} id={9*id+3} click={click} />
            <Tile state={board[3]} id={9*id+4} click={click} />
            <Tile state={board[4]} id={9*id+5} click={click} />
            <Tile state={board[5]} id={9*id+6} click={click} />
            <Tile state={board[6]} id={9*id+7} click={click} />
            <Tile state={board[7]} id={9*id+8} click={click} />
            <Tile state={board[8]} id={9*id+9} click={click} />
        </div>
    )
}

export default MiniBoard;