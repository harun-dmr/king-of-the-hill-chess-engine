"use client";

import { useState, useCallback } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import type { Square } from "chess.js";

const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

const ALGORITHMS = [
  {
    value: "pvs_multi_sort_qs",
    label: "PVS + Quiescence + Multi-Threading",
    description: "Stärkste — empfohlen",
  },
  {
    value: "pvs_multi_sort",
    label: "PVS + Move Ordering + Multi-Threading",
    description: "Stark, ohne Quiescence Search",
  },
  {
    value: "pvs_sort_qs",
    label: "PVS + Move Ordering + Quiescence",
    description: "Stark, single-threaded",
  },
  {
    value: "pvs_sort",
    label: "PVS + Move Ordering",
    description: "PVS mit Zugsortierung",
  },
  {
    value: "pvs",
    label: "PVS (Principal Variation Search)",
    description: "Einfaches PVS",
  },
  {
    value: "alpha_beta_tt",
    label: "Alpha-Beta + Transpositionstabelle",
    description: "Alpha-Beta mit Caching",
  },
  {
    value: "alpha_beta_sorted",
    label: "Alpha-Beta + Move Ordering",
    description: "Alpha-Beta mit Zugsortierung",
  },
  {
    value: "alpha_beta",
    label: "Alpha-Beta",
    description: "Klassisches Alpha-Beta",
  },
  {
    value: "minimax",
    label: "Minimax",
    description: "Einfachster Algorithmus",
  },
  {
    value: "mcts",
    label: "Monte Carlo Tree Search",
    description: "Zufallsbasierte Suche",
  },
];

// Highlight the 4 King of the Hill center squares
const HILL_SQUARES: Record<string, React.CSSProperties> = {
  d4: { backgroundColor: "rgba(234, 179, 8, 0.25)" },
  d5: { backgroundColor: "rgba(234, 179, 8, 0.25)" },
  e4: { backgroundColor: "rgba(234, 179, 8, 0.25)" },
  e5: { backgroundColor: "rgba(234, 179, 8, 0.25)" },
};

export default function ChessEngine() {
  const [game, setGame] = useState(() => new Chess());
  const [fen, setFen] = useState(STARTING_FEN);
  const [fenInput, setFenInput] = useState(STARTING_FEN);
  const [algorithm, setAlgorithm] = useState("pvs_multi_sort_qs");
  const [timeLimit, setTimeLimit] = useState(5);
  const [bestMove, setBestMove] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [moveArrow, setMoveArrow] = useState<[Square, Square, string][]>([]);
  const [highlightSquares, setHighlightSquares] = useState<Record<string, React.CSSProperties>>({});

  const applyPosition = useCallback((newFen: string) => {
    try {
      const newGame = new Chess(newFen);
      setGame(newGame);
      setFen(newFen);
      setFenInput(newFen);
      setBestMove(null);
      setMoveArrow([]);
      setHighlightSquares({});
      setError(null);
    } catch {
      setError("Ungültiger FEN-String");
    }
  }, []);

  const onPieceDrop = useCallback(
    (sourceSquare: string, targetSquare: string) => {
      try {
        const newGame = new Chess(game.fen());
        const move = newGame.move({
          from: sourceSquare as Square,
          to: targetSquare as Square,
          promotion: "q",
        });
        if (move === null) return false;
        const newFen = newGame.fen();
        setGame(newGame);
        setFen(newFen);
        setFenInput(newFen);
        setBestMove(null);
        setMoveArrow([]);
        setHighlightSquares({});
        return true;
      } catch {
        return false;
      }
    },
    [game]
  );

  const getBestMove = async () => {
    setLoading(true);
    setError(null);
    setBestMove(null);
    setMoveArrow([]);
    setHighlightSquares({});

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/best-move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fen, algorithm, time_limit: timeLimit }),
      });

      const data = await res.json();

      if (data.success) {
        const move: string = data.move;
        setBestMove(move);

        if (move.length >= 4) {
          const from = move.slice(0, 2);
          const to = move.slice(2, 4);
          setMoveArrow([[from as Square, to as Square, "#22c55e"]]);
          setHighlightSquares({
            [from]: { backgroundColor: "rgba(34, 197, 94, 0.3)" },
            [to]: { backgroundColor: "rgba(34, 197, 94, 0.5)" },
          });
        }
      } else {
        setError(data.error ?? "Unbekannter Fehler");
      }
    } catch {
      setError("Backend nicht erreichbar. Läuft der Server auf Port 8000?");
    } finally {
      setLoading(false);
    }
  };

  const selectedAlgo = ALGORITHMS.find((a) => a.value === algorithm);

  return (
    <div className="flex flex-col lg:flex-row gap-8 items-start">
      {/* Chessboard */}
      <div className="flex-shrink-0">
        <div className="rounded-lg overflow-hidden shadow-2xl">
          <Chessboard
            position={fen}
            onPieceDrop={onPieceDrop}
            customArrows={moveArrow}
            customSquareStyles={{ ...HILL_SQUARES, ...highlightSquares }}
            boardWidth={480}
            customDarkSquareStyle={{ backgroundColor: "#4a7c59" }}
            customLightSquareStyle={{ backgroundColor: "#f0d9b5" }}
          />
        </div>
        <div className="mt-3 flex gap-2">
          <button
            onClick={() => applyPosition(STARTING_FEN)}
            className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors"
          >
            Startposition
          </button>
          <button
            onClick={() => { setBestMove(null); setMoveArrow([]); setHighlightSquares({}); }}
            className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors"
          >
            Markierung löschen
          </button>
        </div>
        <p className="mt-2 text-xs text-yellow-500/80">
          ■ Gelbe Felder = King of the Hill Zielfelder (d4, d5, e4, e5)
        </p>
      </div>

      {/* Controls */}
      <div className="flex-1 flex flex-col gap-5 min-w-0 w-full lg:max-w-sm">
        {/* FEN Input */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1.5">
            FEN-String
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={fenInput}
              onChange={(e) => setFenInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && applyPosition(fenInput)}
              className="flex-1 min-w-0 bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-xs font-mono focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              placeholder="FEN-String eingeben..."
              spellCheck={false}
            />
            <button
              onClick={() => applyPosition(fenInput)}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-md text-sm font-medium transition-colors whitespace-nowrap"
            >
              Laden
            </button>
          </div>
        </div>

        {/* Algorithm */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1.5">
            Algorithmus
          </label>
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
          >
            {ALGORITHMS.map((a) => (
              <option key={a.value} value={a.value}>
                {a.label}
              </option>
            ))}
          </select>
          {selectedAlgo && (
            <p className="mt-1 text-xs text-gray-500">{selectedAlgo.description}</p>
          )}
        </div>

        {/* Time Limit */}
        <div>
          <div className="flex justify-between mb-1.5">
            <label className="text-sm font-medium text-gray-300">Bedenkzeit</label>
            <span className="text-sm font-bold text-white">{timeLimit}s</span>
          </div>
          <input
            type="range"
            min={1}
            max={30}
            step={1}
            value={timeLimit}
            onChange={(e) => setTimeLimit(Number(e.target.value))}
            className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-blue-500 bg-gray-700"
          />
          <div className="flex justify-between text-xs text-gray-600 mt-1">
            <span>1s (schnell)</span>
            <span>30s (stark)</span>
          </div>
        </div>

        {/* Calculate Button */}
        <button
          onClick={getBestMove}
          disabled={loading}
          className="w-full py-3 bg-green-600 hover:bg-green-500 active:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-md font-semibold text-sm transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Berechne besten Zug...
            </>
          ) : (
            "Besten Zug berechnen"
          )}
        </button>

        {/* Result */}
        {bestMove && (
          <div className="bg-gray-800 border border-green-500/40 rounded-md p-4">
            <p className="text-xs text-gray-400 mb-1 uppercase tracking-wide">Bester Zug</p>
            <p className="text-4xl font-mono font-bold text-green-400">{bestMove}</p>
            <p className="text-xs text-gray-500 mt-2">
              Grüner Pfeil und Felder auf dem Brett markiert
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-red-950/50 border border-red-500/40 rounded-md p-3">
            <p className="text-sm text-red-400">{error}</p>
          </div>
        )}

        {/* Info */}
        <div className="bg-gray-800/60 border border-gray-700/50 rounded-md p-4 text-sm text-gray-400 mt-auto">
          <p className="font-semibold text-gray-200 mb-1">King of the Hill</p>
          <p className="text-xs leading-relaxed">
            Gewinne durch Schachmatt <em>oder</em> indem dein König eines der vier
            Mittelfelder (d4, d5, e4, e5) erreicht.
          </p>
        </div>
      </div>
    </div>
  );
}
