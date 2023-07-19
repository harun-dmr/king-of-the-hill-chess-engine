import copy
import time
import multiprocessing

from core.eval import evaluate_board
from core.utils import Board
from core.zuggenerator import generate, game_ending, gen_all_masks

# Define the function that will be executed by each process
def evaluate_moves_multi(board, moves, alpha, beta, depth, stop_time):
    gen_all_masks()

    move_count = 0
    best_move = None

    bSearchPv = True
    all_moves = moves

    for move in all_moves:
        board_copy = copy.deepcopy(board)
        board_copy.do_move(move)

        if bSearchPv:
            score, _, mc = pvsuche_multi(board_copy, -beta, -alpha, depth - 1, stop_time)
            score = -score
            move_count += mc
        else:
            score, _, mc = pvsuche_multi(board_copy, -alpha - 1, -alpha, depth - 1, stop_time)
            score = -score
            move_count += mc
            if score > alpha:
                score, _, mc = pvsuche_multi(board_copy, -beta, -alpha, depth - 1, stop_time)
                score = -score
                move_count += mc

        if score >= beta:
            return beta, move, move_count  # Fail-hard beta-cutoff
        if score > alpha:
            alpha = score
            best_move = move
            bSearchPv = False

    return alpha, best_move, move_count  # Fail-hard

def pvs_multi(board, time_limit):
    stop_time = time.time() + time_limit
    glob_best_move = None
    depth = 1
    while time.time() < stop_time:
        t1 = time.time()
        _, best_move, move_count = pvsuche_first_multi(board, float('-inf'), float('inf'), depth, stop_time)
        t2 = time.time()
        if best_move is not None and time.time() < stop_time:
            print(f"depth: {depth},     time: {round(t2 - t1, 4)}s,   zustände: {move_count}")
        depth += 1
        if best_move is not None:
            glob_best_move = best_move

    return glob_best_move

def pvsuche_first_multi(board, alpha, beta, depth, stop_time):
    best_move = None
    all_moves = generate(board)

    # Divide the moves into chunks for multiprocessing
    chunk_size = max(1, len(all_moves) // multiprocessing.cpu_count())
    move_chunks = [all_moves[i:i + chunk_size] for i in range(0, len(all_moves), chunk_size)]

    # Create a multiprocessing Pool with the number of available CPU cores
    with multiprocessing.Pool() as pool:
        results = pool.starmap(evaluate_moves_multi, [(board, moves, -beta, -alpha, depth, stop_time) for moves in move_chunks])

    move_count = 0

    for score, move, mc in results:
        move_count += mc
        if score >= beta:
            return beta, move, move_count # Fail-hard beta-cutoff
        if score > alpha:
            alpha = score
            best_move = move

    return alpha, best_move, move_count  # Fail-hard

def pvsuche_multi(board, alpha, beta, depth, stop_time):
    move_count = 0

    best_move = None
    if depth == 0 or game_ending(board) or stop_time < time.time():
        return evaluate_board(board, sym=True), best_move, 1

    bSearchPv = True
    all_moves = generate(board)

    for move in all_moves:
        board_copy = copy.deepcopy(board)
        board_copy.do_move(move)

        if bSearchPv:
            score, _, mc = pvsuche_multi(board_copy, -beta, -alpha, depth - 1, stop_time)
            score = -score
            move_count += mc
        else:
            score, _, mc = pvsuche_multi(board_copy, -alpha - 1, -alpha, depth - 1, stop_time)
            score = -score
            move_count += mc
            if score > alpha:
                score, _, mc = pvsuche_multi(board_copy, -beta, -alpha, depth - 1, stop_time)
                score = -score
                move_count += mc

        if score >= beta:
            return beta, move, move_count  # Fail-hard beta-cutoff
        if score > alpha:
            alpha = score
            best_move = move
            bSearchPv = False

    return alpha, best_move, move_count  # Fail-hard



if __name__ == "__main__":
    import time

    gen_all_masks()
    time_limit = 5
    #fen1 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"
    #fen2 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    fen1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    fen2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"
    print("--------   pvs   --------")
    board1 = Board(fen1)
    print(board1)
    print("------------------------")
    print("PVS", pvs_multi(board1, 1, time_limit))
    board2 = Board(fen2)
    print("PVS", pvs_multi(board2, 1, time_limit))
