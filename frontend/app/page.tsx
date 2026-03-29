import dynamic from "next/dynamic";

// react-chessboard uses browser APIs — load only on client
const ChessEngine = dynamic(() => import("./components/ChessEngine"), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-64 text-gray-500">
      Lade Schachbrett...
    </div>
  ),
});

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950">
      <div className="max-w-5xl mx-auto px-4 py-10">
        {/* Header */}
        <header className="mb-10">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">♟</span>
            <h1 className="text-3xl font-bold tracking-tight">
              King of the Hill Chess Engine
            </h1>
          </div>
          <p className="text-gray-400 text-sm">
            TU Berlin · Symbolic AI Project · Sommersemester 2023 &nbsp;·&nbsp;
            Implemented algorithms: PVS, Alpha-Beta, Minimax, MCTS
          </p>
        </header>

        {/* Main content */}
        <ChessEngine />

        {/* Footer */}
        <footer className="mt-16 pt-6 border-t border-gray-800 text-xs text-gray-600 flex flex-wrap gap-4 justify-between">
          <span>Built with Next.js · FastAPI · react-chessboard</span>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-400 transition-colors"
          >
            GitHub →
          </a>
        </footer>
      </div>
    </main>
  );
}
