import React, { useState, useEffect } from "react";
import Board from "./Board";

function MyApp() {
    const [board, setBoard] = useState(
        Array.from({ length: 9 }, () => Array(9).fill(0))
    );
    const [cur_move_type, setCur_mov_type] = useState(0);
    const [board_wins, setBoard_wins] = useState(Array(9).fill(0));

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
                console.log(data);
                setBoard(data.board);
                setCur_mov_type(data.cur_move_type);
                setBoard_wins(data.board_wins);
            })
            .catch((error) => {
                console.error("Error occurred:", error);
            });
    }

    function reset() {
        fetch("http://localhost:8000/reset", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            }
        })
            .then((response) => {
                if (response.status === 200) {
                    return response.json();
                }
            })
            .then((data) => {
                setBoard(data.board);
                setCur_mov_type(data.cur_move_type);
                setBoard_wins(data.board_wins);
            })
            .catch((error) => {
                console.error("Error occurred:", error);
            });
    }

    useEffect(() => {
        const handleKeyPress = (event) => {
            if (event.key === "r" || event.key === "R") {
                reset();
            }
        };

        window.addEventListener("keydown", handleKeyPress);

        return () => {
            window.removeEventListener("keydown", handleKeyPress);
        };
    }, []);

    return (
        <div>
            <h1>Ultimate Tic-Tac-Toe</h1>
            <Board board={board} click={click} cur_move_type={cur_move_type} board_wins={board_wins} />
        </div>
    );
}

export default MyApp;