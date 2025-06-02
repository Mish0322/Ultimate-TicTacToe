import React, { useState, useEffect } from "react";
import Board from "./Board";

function MyApp() {
  const [board, setBoard] = useState(
    Array.from({ length: 9 }, () => Array(9).fill(0))
  );
  const [cur_move_type, setCur_mov_type] = useState(0);
  const [board_wins, setBoard_wins] = useState(Array(9).fill(0));
  const [winner, setWinner] = useState(0);
  const [suggestedMoves, setSuggestedMoves] = useState(null);

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
        setBoard([...data.board]);
        setCur_mov_type(data.cur_move_type);
        setBoard_wins(data.board_wins);
        setWinner(data.winner);
      })
      .catch((error) => {
        console.error("Error occurred:", error);
      });
  }

  function fetchSuggestedMoves() {
    fetch("http://localhost:8000/suggest_moves")
      .then((res) => res.json())
      .then((data) => {
        setSuggestedMoves(data);
      })
      .catch((error) => console.error("Error fetching suggestions:", error));
  }

  function playSuggestedMove(move) {
    const moveObj = { square: move };
    fetch("http://localhost:8000/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(moveObj),
    })
      .then((res) => res.json())
      .then((data) => {
        setBoard(data.board);
        setCur_mov_type(data.cur_move_type);
        setBoard_wins(data.board_wins);
        setWinner(data.winner);
        setSuggestedMoves(null);
      })
      .catch((error) => console.error("Error playing suggested move:", error));
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
        <div className="button-row">
          <button onClick={makeRandomMove}>Opponent Random Move</button>
          <button onClick={fetchSuggestedMoves}>Get Suggested Moves</button>
        </div>

        {suggestedMoves && (
          <div style={{ marginTop: "1rem" }}>
            <h3>Choose Suggested Move:</h3>
            <ul style={{ listStyleType: "none", padding: 0 }}>
              <li>
                Minimax One:{" "}
                <button
                  className="suggestion-button"
                  onClick={() =>
                    playSuggestedMove(suggestedMoves.minimax_one.move)
                  }
                >
                  Play (Mini-board {suggestedMoves.minimax_one.mini_board}, Cell{" "}
                  {suggestedMoves.minimax_one.cell})
                </button>
              </li>
              <li>
                Minimax Two:{" "}
                <button
                  className="suggestion-button"
                  onClick={() =>
                    playSuggestedMove(suggestedMoves.minimax_two.move)
                  }
                >
                  Play (Mini-board {suggestedMoves.minimax_two.mini_board}, Cell{" "}
                  {suggestedMoves.minimax_two.cell})
                </button>
              </li>
              <li>
                MCTS:{" "}
                <button
                  className="suggestion-button"
                  onClick={() => playSuggestedMove(suggestedMoves.mcts.move)}
                >
                  Play (Mini-board {suggestedMoves.mcts.mini_board}, Cell{" "}
                  {suggestedMoves.mcts.cell})
                </button>
              </li>
            </ul>
          </div>
        )}

        {winner !== 0 && (
          <div className="popup">
            <div className="popup-inner">
              {winner === 3 ? (
                <h2 className="winner">It's a Tie!</h2>
              ) : (
                <h2 className="winner">Player {winner} wins!</h2>
              )}
              <button onClick={reset}>
                Play Again
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MyApp;
