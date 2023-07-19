import copy
import time

from core.utils import Board, Move
from core.zuggenerator import generate, game_ending, gen_all_masks, sort_moves
from core.eval import evaluate_board


def iterative_deepening_alpha_beta_sorted(board: Board, time_limit: float) -> Move:
    best_move = None
    max_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    stop_time = time.time() + time_limit
    depth = 1

    while time.time() < stop_time:
        t1 = time.time()
        score, move, zustaende = alpha_beta_sorted(board, depth, alpha, beta, stop_time)
        t2 = time.time()
        if score > max_score and time.time() < stop_time:
            max_score = score
            best_move = move
        if best_move is not None:
            print(f"depth: {depth},     time: {round(t2 - t1, 4)}s,   zustände: {zustaende}")
        depth += 1

    return best_move





def alpha_beta_sorted(board: Board, depth: int, alpha: float, beta: float, stop_time: float, move: Move = None) -> (float, Move, int):
    # if depth == 0 or game_ending(board):
    #     return eval_move(board, move), None

    # def key_alpha_beta_sorted(move: Move):
    #     b = copy.deepcopy(board)
    #     b.do_move(move)
    #     return evaluate_board(b)

    best_move = None
    unsorted_moves = generate(board)
    moves = sort_moves(unsorted_moves)
    zuege = 0

    if board.active_color:
        max_score = float('-inf')

        for move in moves:
            board_copy = copy.deepcopy(board)
            if depth == 0 or game_ending(board) or stop_time < time.time():
                if stop_time < time.time():
                    temp_board = copy.deepcopy(board)
                    temp_board.do_move(move)
                    return evaluate_board(temp_board), None, zuege
                temp_board = copy.deepcopy(board)
                temp_board.do_move(move)
                return evaluate_board(temp_board), None, 1
            else:
                board_copy.do_move(move)
                score, _, z = alpha_beta_sorted(board_copy, depth - 1, alpha, beta, stop_time)
                zuege += z

            if score > max_score:
                max_score = score
                best_move = move

            alpha = max(alpha, max_score)
            if alpha >= beta:
                break

        return max_score, best_move, zuege
    else:

        min_score = float('inf')

        for move in moves:
            board_copy = copy.deepcopy(board)
            if depth == 0 or game_ending(board) or stop_time < time.time():
                if stop_time < time.time():
                    temp_board = copy.deepcopy(board)
                    temp_board.do_move(move)
                    return evaluate_board(temp_board), None, zuege
                temp_board = copy.deepcopy(board)
                temp_board.do_move(move)
                return evaluate_board(temp_board), None, 1
            else:
                board_copy.do_move(move)
                score, _, z = alpha_beta_sorted(board_copy, depth - 1, alpha, beta, stop_time)
                zuege += z

            if score < min_score:
                min_score = score
                best_move = move

            beta = min(beta, min_score)
            if alpha >= beta:
                break

        return min_score, best_move, zuege

if __name__ == "__main__":
    import time
    gen_all_masks()
    time_limit = 100
    fen1 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"
    fen2 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    print("--------   pvs   --------")
    board1 = Board(fen1)
    print(board1)
    print("------------------------")
    x1 = time.time()
    print("PVS", iterative_deepening_alpha_beta_sorted(board1, 4, time_limit))
    x2 = time.time()
    print("time to calc move using PVS: ", x2 - x1)
    board2 = Board(fen2)
    print(board2)
    x_1 = time.time()
    print("PVS", iterative_deepening_alpha_beta_sorted(board2, 4, time_limit))
    x_2 = time.time()
    print("time to calc move using PVS: ", x_2 - x_1)