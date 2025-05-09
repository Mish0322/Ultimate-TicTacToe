import React, { useState, useEffect } from "react";
import Board from "./Board";

function MyApp() {
    const [board, setBoard] = useState(
        Array.from({ length: 9 }, () => Array(9).fill(0))
    );

    function click(square_id) {
        console.log(square_id);
        const move = { "square": square_id };

        fetch("http://localhost:8000/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(move),
        })
            .then((response) => {
                if (response.status === 200) {
                    return response.json();
                }
            })
            .then((data) => {
                setBoard(data.board);
            })
            .catch((error) => {
                console.error("Error occurred:", error);
            });
    }

    return (
        <div>
            <h1>Ultimate Tic-Tac-Toe</h1>
            <Board board={board} click={click} />
        </div>
    );
}

export default MyApp;