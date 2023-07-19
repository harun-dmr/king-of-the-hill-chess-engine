import time
import copy

from core.utils import Board, Move
from core.zuggenerator import generate, game_ending
from core.eval import evaluate_board





def minimax(board: Board, max_depth: int, time_limit: float) -> Move:
    best_move = None
    max_score = float('-inf')
    stop_time = time.time() + time_limit
    depth = 1

    while time.time() < stop_time:
        t1 = time.time()
        score, move, zuege = minimax_rec(board, depth, stop_time)
        t2 = time.time()
        if score > max_score and time.time() < stop_time:
            max_score = score
            best_move = move
        if best_move is not None:
            print(f"depth: {depth},     time: {t2 - t1}s,   zustände: {zuege}")
        depth += 1

    return best_move


def minimax_rec(board: Board, depth: int, stop_time: float, move: Move = None) -> (float, Move, int):
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
                score, _, z = minimax_rec(board_copy, depth - 1, stop_time)
                zuege += z

            if score > max_score:
                max_score = score
                best_move = move

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
                score, _, z = minimax_rec(board_copy, depth - 1, stop_time)
                zuege += z

            if score < min_score:
                min_score = score
                best_move = move

        return min_score, best_move, zuege





def minimax_id(board: Board, time_limit: int) -> Move:
    """
    Minimax using iterative deepening. Executes till a certain time limit

    :param time_limit: the time limit for the minimax search in seconds.
    :return: the best move calculated by minimax.
    """
    depth = 1
    move = None

    stop_time = time.time() + time_limit

    while time.time() <= stop_time:
        #print(time.time(), stop_time)
        res_move = minimax(board, depth, stop_time)
        if not time.time() < stop_time:
            move = res_move
        depth += 1

    return move