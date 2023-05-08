import React, { Fragment, useState } from "react";

function Square({value, onSquareClick}) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

function Board({xIsNext, squares, onPlay, move, mode, pastSquare, needToWin}) {
  const afterThreeMoves = (move >= 6);

  function normalRules(i) {
    if (squares[i]) {
      return;
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = "X";
    } else {
      nextSquares[i] = "O";
    }
    onPlay(nextSquares, false, i, false);
  }

  function chorusRules(i) {
    //variables
    const curValue = (move % 2) === 0 ? "X" : "O";

    //first check if selection mode is active
    if (mode) {
      if(adjacentSquare(pastSquare, i)) {
        if (needToWin) {
          const emptyAdjacents = availableAdjacents(pastSquare, squares);
          const winners = possibleWinners(emptyAdjacents, curValue, pastSquare, squares);
          if (!winners.includes(i)) {
            return;
          }
        }
        normalRules(i);
      }
      else {
        return;
      }
    }
    //if it isn't pick piece to be moved
    else {
      //check for valid piece
      const emptyAdjacents = availableAdjacents(i, squares);
      if (curValue !== squares[i] || emptyAdjacents.length < 1) {
        return;
      }
      let needWin = false;
      //check for occupation of center square:
      if (curValue === squares[4] && i!==4) {
        const winners = possibleWinners(emptyAdjacents, curValue, i, squares);
        if (winners.length < 1) {
          return;
        }
        needWin = true;
      }
      const nextSquares = squares.slice();
      nextSquares[i] = null;
      onPlay(nextSquares, true, i, needWin);
    }
  }

  function handleClick(i) {
    if (calculateWinner(squares)) {
      return;
    }
    if (!afterThreeMoves) {
      normalRules(i);
    } else {
      chorusRules(i);
    }
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O");
  }
    return (
    <Fragment>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </Fragment>
    );
}

export default function Game() {
  const [squares, setSquares] = useState(Array(9).fill(null)); //current square values
  const [currentMove, setCurrentMove] = useState(0); //current move number
  const xIsNext = currentMove % 2 === 0;
  const [selectionMode, setSelectionMode] = useState(false);
  const [pastSquare, setPastSquare] = useState(0); //square # of picked up piece
  const [needToWin, setNeedToWin] = useState(false); 

  function handlePlay(nextSquares, nextMode, currentSquare, needToWin) {
    setSelectionMode(nextMode);
    setSquares(nextSquares);
    if (!nextMode) {
      setCurrentMove(currentMove + 1);
    }
    setPastSquare(currentSquare);
    setNeedToWin(needToWin);
  }

  return (
    <div className="game">
      <div className="game-board">
        <Board 
        xIsNext={xIsNext} squares={squares} onPlay={handlePlay} 
        move={currentMove} mode={selectionMode} pastSquare={pastSquare} needToWin={needToWin}
        />
      </div>
    </div>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

const adjacents = [
  [1, 3, 4],
  [0, 2, 3, 4, 5],
  [1, 4, 5],
  [0, 1, 4, 6, 7], 
  [0, 1, 2, 3, 5, 6, 7, 8],
  [1, 2, 4, 7, 8],
  [3, 4, 7],
  [3, 4, 5, 6, 8],
  [4, 5, 7],
]
  
//returns true if target square is adjacent to past square
function adjacentSquare(past, target) {
  return (adjacents[past].includes(target));
}

//returns true if at least one square adjacent to cur is empty
function availableAdjacents(cur, squares) {
  let adj = [];
  for (let i = 0; i < adjacents[cur].length; i++) {
    if (squares[adjacents[cur][i]] === null) {
      adj = [...adj, adjacents[cur][i]];
    }
  }
  return adj;
}

//adj: list of empty adjacent squares
//returns a list of square indices curSquare could move to to win
function possibleWinners(adj, curValue, curSquare, squares) {
  let winners = [];
  for (let i = 0; i < adj.length; i++) {
    const nextSquares = squares.slice();
    nextSquares[curSquare] = null;
    nextSquares[adj[i]] = curValue;
    if (calculateWinner(nextSquares)) {
      winners = [...winners, adj[i]]
    }
  }
  return winners;
}
