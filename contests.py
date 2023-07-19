import time

from core.utils import Board
from core.zuggenerator import game_ending, check_king_hill, check_for_remi, check_for_checkmate, gen_all_masks
from core.dtm import dynamic_time_management

from core.aitech.alpha_beta.alpha_beta import iterative_deepening_alpha_beta_search
from core.aitech.alpha_beta.alpha_beta_tt import iterative_deepening_alpha_beta_TT
from core.aitech.alpha_beta.alpha_beta_sorted import iterative_deepening_alpha_beta_sorted
from core.aitech.pvs.pvs import pvs
from core.aitech.mcts import mcts
from core.aitech.pvs.pvs_sorted import pvs_sort
from core.aitech.pvs.pvs_sorted_multi import pvs_multi_sort
from core.aitech.pvs.pvs_sorted_multi_qs import pvs_multi_sort_qs as pvs_multi_sort_qs
from core.aitech.pvs.pvs_sorted_qs import pvs_sort_qs as pvs_sort_qs


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"


def play_clock(player_1_function, player_2_function, chess_clock_time=300):
    with open("contest_results.dat", "a") as file:
        file.write("----    NEW GAME    ----\n")
        file.write(f"time per player: {chess_clock_time}\n")
        file.write(f"player 1: {player_1_function.__name__}\n")
        file.write(f"player 2: {player_2_function.__name__}\n")

    board = Board(START_FEN)

    p1_time = chess_clock_time
    p2_time = chess_clock_time

    for i in range(200):
        tl = dynamic_time_management(board=board, time=p1_time)
        t1 = time.time()
        move = player_1_function(board=board, time_limit=tl)
        print(move)
        t2 = time.time()
        p1_time -= (t2 - t1)
        board.do_move(move)
        if game_ending(board):
            with open("contest_results.dat", "a") as file:
                file.write("Game Ended. Winner: Player 1\n")
                if check_for_remi(board):
                    file.write("Reason: Remi\n")
                elif check_for_checkmate(board):
                    file.write("Reason: Checkmate\n")
                elif check_king_hill(board):
                    file.write("Reason: King Hill\n")
                file.write(f"Time Left. Player 1: {p1_time}, Player 2: {p2_time}\n")
            return


        if p1_time <= 0:
            with open("contest_results.dat", "a") as file:
                file.write(" Game Ended. Winner: Player 2\n")
                file.write("Reason: No time left for Player 1\n")
                file.write(f"Time Left. Player 1: {p1_time}, Player 2: {p2_time}\n")
            return

        tl = dynamic_time_management(board=board, time=p2_time)
        t1 = time.time()
        move = player_2_function(board=board, time_limit=tl)
        print(move)
        t2 = time.time()
        p2_time -= (t2 - t1)
        board.do_move(move)
        if game_ending(board):
            with open("contest_results.dat", "a") as file:
                file.write("Game Ended. Winner: Player 2\n")
                if check_for_remi(board):
                    file.write("Reason: Remi\n")
                elif check_for_checkmate(board):
                    file.write("Reason: Checkmate\n")
                elif check_king_hill(board):
                    file.write("Reason: King Hill\n")
                file.write(f"Time Left. Player 1: {p1_time}, Player 2: {p2_time}\n")
            return


        if p1_time <= 0:
            with open("contest_results.dat", "a") as file:
                file.write(" Game Ended. Winner: Player 1\n")
                file.write("Reason: No time left for Player 2\n")
                file.write(f"Time Left. Player 1: {p1_time}, Player 2: {p2_time}\n")
            return

    with open("contest_results.dat", "a") as file:
        file.write("Game did not End after 200 Moves. Abort.\n")

    return



def play(player_1_function, player_2_function, chess_clock_time=30):
    with open("contest_results.dat", "a") as file:
        file.write("----    NEW GAME FIXED TIME    ----\n")
        file.write(f"player 1: {player_1_function.__name__}\n")
        file.write(f"player 2: {player_2_function.__name__}\n")

    REMI_D = {}

    board = Board(START_FEN)


    for i in range(200):
        move = player_1_function(board=board, time_limit=chess_clock_time)
        board.do_move(move)
        if game_ending(board):
            with open("contest_results.dat", "a") as file:
                file.write("Game Ended. Winner: Player 1\n")
                if check_for_remi(board):
                    file.write("Reason: Remi\n")
                elif check_for_checkmate(board):
                    file.write("Reason: Checkmate\n")
                elif check_king_hill(board):
                    file.write("Reason: King Hill\n")
            return
        if move.capture:
            REMI_D = {}
        else:
            if hash(board) in REMI_D:
                REMI_D[hash(board)] = REMI_D[hash(board)] + 1
                if REMI_D[hash(board)] == 3:
                    with open("contest_results.dat", "a") as file:
                        file.write("Game Ended. No Winner")
                        file.write("Reason: Real Remi --\n")
                    return
            else:
                REMI_D[hash(board)]= 1

        move = player_2_function(board=board, time_limit=chess_clock_time)
        board.do_move(move)
        if game_ending(board):
            with open("contest_results.dat", "a") as file:
                file.write("Game Ended. Winner: Player 2\n")
                if check_for_remi(board):
                    file.write("Reason: Remi\n")
                elif check_for_checkmate(board):
                    file.write("Reason: Checkmate\n")
                elif check_king_hill(board):
                    file.write("Reason: King Hill\n")
            return

        if move.capture:
            REMI_D = {}
        else:
            if hash(board) in REMI_D:
                REMI_D[hash(board)] = REMI_D[hash(board)] + 1
                if REMI_D[hash(board)] == 3:
                    with open("contest_results.dat", "a") as file:
                        file.write("Game Ended. No Winner")
                        file.write("Reason: Real Remi --\n")
                    return
            else:
                REMI_D[hash(board)]= 1

    with open("contest_results.dat", "a") as file:
        file.write("Game did not End after 200 Moves. Abort.\n")

    return



def start_contest(chess_clock_time=300):
    try:
        play(player_1_function=mcts, player_2_function=pvs_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=mcts, player_2_function=pvs_multi_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=mcts, player_2_function=pvs_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=mcts, player_2_function=pvs_multi_sort_qs, chess_clock_time=chess_clock_time)
    except Exception as e:
        with open("contest_results.dat", "a") as file:
            file.write(f"Exception in 1: {e}\n")

    try:
        play(player_1_function=pvs_sort, player_2_function=pvs_multi_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_sort, player_2_function=pvs_multi_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_sort, player_2_function=pvs_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_sort, player_2_function=mcts, chess_clock_time=chess_clock_time)
    except Exception as e:
        with open("contest_results.dat", "a") as file:
            file.write(f"Exception in 2: {e}\n")

    try:
        play(player_1_function=pvs_multi_sort, player_2_function=pvs_multi_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_multi_sort, player_2_function=pvs_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_multi_sort, player_2_function=pvs_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_multi_sort, player_2_function=mcts, chess_clock_time=chess_clock_time)
    except Exception as e:
        with open("contest_results.dat", "a") as file:
            file.write(f"Exception in 3: {e}\n")

    try:
        play(player_1_function=pvs_sort_qs, player_2_function=pvs_multi_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_sort_qs, player_2_function=pvs_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_sort_qs, player_2_function=pvs_multi_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_sort_qs, player_2_function=mcts, chess_clock_time=chess_clock_time)
    except Exception as e:
        with open("contest_results.dat", "a") as file:
            file.write(f"Exception in 4: {e}\n")

    try:
        play(player_1_function=pvs_multi_sort_qs, player_2_function=pvs_sort_qs, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_multi_sort_qs, player_2_function=pvs_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_multi_sort_qs, player_2_function=pvs_multi_sort, chess_clock_time=chess_clock_time)
        play(player_1_function=pvs_multi_sort_qs, player_2_function=mcts, chess_clock_time=chess_clock_time)
    except Exception as e:
        with open("contest_results.dat", "a") as file:
            file.write(f"Exception in 5: {e}\n")



if __name__ == "__main__":
    gen_all_masks()
    start_contest(7)
