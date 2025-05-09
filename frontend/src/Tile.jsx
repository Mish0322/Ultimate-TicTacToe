import React from "react";

function Tile({ state, id, click }) {

  let val = "";
  if (state === 1) {
    val = "X";
  } else if (state === 2) {
    val = "O";
  }

  return (
    <div className="tile" onClick={() => click(id)}>
      <h1>{val}</h1>
    </div>
  );
}

export default Tile;