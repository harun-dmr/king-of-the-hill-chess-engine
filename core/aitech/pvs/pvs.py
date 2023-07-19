import copy
import time

from core.eval import evaluate_board
from core.utils import Board
from core.zuggenerator import generate, game_ending, gen_all_masks

def pvs(board,  time_limit):
    """
    Normal PVS.
    :param board: The board
    :param time_limit: The Time to choose the Move
    :return: Move object, representing best move
    """
    stop_time = time.time() + time_limit
    glob_best_move = None
    depth = 1
    while time.time() < stop_time:
        t1 = time.time()
        _, best_move, move_count = pvsuche(board, float('-inf'), float('inf'), depth, stop_time)
        t2 = time.time()
        if best_move is not None and time.time() < stop_time:
            print(f"depth: {depth},     time: {round(t2 - t1, 4)}s,   zustände: {move_count}")
        depth += 1
        if best_move is not None:
            glob_best_move = best_move

    return glob_best_move


def pvsuche(board, alpha, beta, depth, stop_time):
    best_move = None
    move_count = 0
    if depth == 0 or game_ending(board) or stop_time < time.time():
        return evaluate_board(board, sym=True), best_move, 1  # You need to implement the 'quiesce' function separately

    bSearchPv = True
    all_moves = generate(board)

    for move in all_moves:  # You need to define the 'all_moves' list or generator
        board_copy = copy.deepcopy(board)
        board_copy.do_move(move)  # You need to implement the 'make_move' function

        if bSearchPv:
            score, _, mc = pvsuche(board_copy, -beta, -alpha, depth - 1, stop_time)
            score = -score
            move_count += mc
        else:
            score, _, mc = pvsuche(board_copy, -alpha - 1, -alpha, depth - 1, stop_time)
            score = -score
            move_count += mc
            if score > alpha:  # In fail-soft, 'score < beta' is common, but not included here
                score, _, mc = pvsuche(board_copy, -beta, -alpha, depth - 1, stop_time)  # Re-search
                score = -score
                move_count += mc

        if score >= beta:
            return beta, move, move_count  # Fail-hard beta-cutoff
        if score > alpha:
            alpha = score
            best_move = move
            bSearchPv = False  # *1)

    return alpha, best_move, move_count  # Fail-hard


if __name__ == "__main__":
    import time

    gen_all_masks()
    time_limit = 5
    #fen1 = "3r3k/p4n1p/5NpP/1p2p3/1Q2Pp2/5P2/PP2K1P1/2rR4 w - - 0 1"
    #fen2 = "4rR2/1p1k2pp/2p5/2Pp2q1/3P2P1/pPn5/P1N4P/K3R3 b - - 0 1"
    fen1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    fen2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"
    print("--------   pvs   --------")
    board1 = Board(fen1)
    print(len(generate(board1)))
    print("PVS", pvs(board1, 1, time_limit))
    board2 = Board(fen2)
    print(len(generate(board2)))
    print("PVS", pvs(board2, 1, time_limit))
