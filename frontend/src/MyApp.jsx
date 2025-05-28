import React, { useState, useEffect } from "react";
import Board from "./Board";

function MyApp() {
  const [board, setBoard] = useState(
    Array.from({ length: 9 }, () => Array(9).fill(0))
  );
  const [cur_move_type, setCur_mov_type] = useState(0);
  const [board_wins, setBoard_wins] = useState(Array(9).fill(0));
  const [winner, setWinner] = useState(0);
  function click(square_id) {
    const move = { square: square_id };

    fetch("http://localhost:8000/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(move),
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
        setWinner(data.winner);
        console.log(data.winner);
      })
      .catch((error) => {
        console.error("Error occurred:", error);
      });
  }

  function reset() {
    fetch("http://localhost:8000/reset", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
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
        setWinner(data.winner);
      })
      .catch((error) => {
        console.error("Error occurred:", error);
      });
  }

  function makeRandomMove() {
    fetch("http://localhost:8000/random_move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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
        setWinner(data.winner);
      })
      .catch((error) => {
        console.error("Error occurred:", error);
      });
  }

  function makeBestMoveFull() {
    fetch("http://localhost:8000/best_move_full", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((data) => {
        setBoard(data.board);
        setCur_mov_type(data.cur_move_type);
        setBoard_wins(data.board_wins);
        setWinner(data.winner);
      });
  }

  function makeBestMove() {
    fetch("http://localhost:8000/best_move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((data) => {
        setBoard(data.board);
        setCur_mov_type(data.cur_move_type);
        setBoard_wins(data.board_wins);
        setWinner(data.winner);
      });
  }

  function simRvDLMM() {
    fetch("http://localhost:8000/sim_R_v_DLMM", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((data) => {
        setBoard(data.board);
        setCur_mov_type(data.cur_move_type);
        setBoard_wins(data.board_wins);
        setWinner(data.winner);
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
      <Board
        board={board}
        click={click}
        cur_move_type={cur_move_type}
        board_wins={board_wins}
      />
      <div style={{ marginTop: "1rem" }}>
        <button onClick={makeRandomMove}>Opponent Random Move</button>
        <button onClick={makeBestMoveFull}>Opponent Best Move (Full MiniMax WARNING)</button>
        <button onClick={makeBestMove}>Opponent Best Move (DL MiniMax)</button>
        <button onClick={simRvDLMM}>Simulate</button>
        {winner !== 0 && (
          <div className="popup">
            <div className="popup-inner">
              {winner === 3 ? (
                <h2 className="winner">It’s a Tie!</h2>
              ) : (
                <h2 className="winner">Player {winner} wins!</h2>
              )}
              <button onClick={reset}>Play Again</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MyApp;
