import sys
import os

# Add project root to path so we can import core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from core.utils import Board
from core.zuggenerator import gen_all_masks
from core.aitech.pvs.pvs_sorted_multi_qs import pvs_multi_sort_qs
from core.aitech.pvs.pvs_sorted_multi import pvs_multi_sort
from core.aitech.pvs.pvs_sorted_qs import pvs_sort_qs
from core.aitech.pvs.pvs_sorted import pvs_sort
from core.aitech.pvs.pvs import pvs
from core.aitech.alpha_beta.alpha_beta_tt import iterative_deepening_alpha_beta_TT
from core.aitech.alpha_beta.alpha_beta_sorted import iterative_deepening_alpha_beta_sorted
from core.aitech.alpha_beta.alpha_beta import iterative_deepening_alpha_beta_search
from core.aitech.minimax import minimax_id
from core.aitech.mcts import mcts

gen_all_masks()

app = FastAPI(title="King of the Hill Chess Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALGORITHMS = {
    "pvs_multi_sort_qs": pvs_multi_sort_qs,
    "pvs_multi_sort":    pvs_multi_sort,
    "pvs_sort_qs":       pvs_sort_qs,
    "pvs_sort":          pvs_sort,
    "pvs":               pvs,
    "alpha_beta_tt":     iterative_deepening_alpha_beta_TT,
    "alpha_beta_sorted": iterative_deepening_alpha_beta_sorted,
    "alpha_beta":        iterative_deepening_alpha_beta_search,
    "minimax":           minimax_id,
    "mcts":              mcts,
}


class MoveRequest(BaseModel):
    fen: str
    algorithm: str = "pvs_multi_sort_qs"
    time_limit: int = Field(default=5, ge=1, le=60)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/best-move")
async def get_best_move(request: MoveRequest):
    try:
        board = Board(request.fen)
    except Exception:
        return {"success": False, "error": "Ungültiger FEN-String"}

    algo_fn = ALGORITHMS.get(request.algorithm)
    if algo_fn is None:
        return {"success": False, "error": f"Unbekannter Algorithmus: {request.algorithm}"}

    try:
        move = await run_in_threadpool(
            algo_fn, board=board, time_limit=request.time_limit
        )
        if move is None:
            return {"success": False, "error": "Kein Zug gefunden (Spiel beendet?)"}
        return {"success": True, "move": str(move)}
    except Exception as e:
        return {"success": False, "error": str(e)}
