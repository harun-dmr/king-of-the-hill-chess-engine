import copy
import time

from core.utils import Board, Move
from core.zuggenerator import generate, game_ending
from core.eval import evaluate_board



def iterative_deepening_alpha_beta_search(board: Board, time_limit: float) -> Move:
    best_move = None
    max_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    stop_time = time.time() + time_limit
    depth = 1

    while time.time() < stop_time:
        t1 = time.time()
        score, move, zustaende = alpha_beta(board, depth, alpha, beta, stop_time)
        t2 = time.time()
        if score > max_score and time.time() < stop_time:
            max_score = score
            best_move = move
        if best_move is not None:
            print(f"depth: {depth},     time: {t2 - t1}s,   zustände: {zustaende}")
        depth += 1

    return best_move


def alpha_beta(board: Board, depth: int, alpha: float, beta: float, stop_time: float, move: Move = None) -> (float, Move, int):
    # if depth == 0 or game_ending(board):
    #     return eval_move(board, move), None

    best_move = None
    moves = generate(board)
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
                score, _, z = alpha_beta(board_copy, depth - 1, alpha, beta, stop_time)
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
                score, _, z = alpha_beta(board_copy, depth - 1, alpha, beta, stop_time)
                zuege += z

            if score < min_score:
                min_score = score
                best_move = move

            beta = min(beta, min_score)
            if alpha >= beta:
                break

        return min_score, best_move, zuege