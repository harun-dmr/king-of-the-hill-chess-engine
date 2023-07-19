import time
import core.utils as ut
from core.zuggenerator import gen_all_masks, generate

from core.aitech.alpha_beta.alpha_beta import iterative_deepening_alpha_beta_search
from core.aitech.alpha_beta.alpha_beta_tt import iterative_deepening_alpha_beta_TT
from core.aitech.alpha_beta.alpha_beta_sorted import iterative_deepening_alpha_beta_sorted
from core.aitech.pvs.pvs import pvs
from core.aitech.mcts import mcts
from core.aitech.pvs.pvs_multi import pvs_multi
from core.aitech.pvs.pvs_sorted import pvs_sort
from core.aitech.pvs.pvs_sorted_multi import pvs_multi_sort
from core.aitech.pvs.pvs_sorted_multi_qs import pvs_multi_sort_qs as pvs_multi_sort_qs
from core.aitech.pvs.pvs_sorted_qs import pvs_sort_qs as pvs_sort_qs


# Position from game Joseph Blackburne–Siegbert Tarrasch, Breslau 1889
MIDDLEGAME = "r2q3k/pn2bprp/4pNpQ/2p1Pb2/3p1P2/5NR1/PPP3PP/2B2RK1 w - - 0 0"
ENDGAME = "8/3np3/3pk3/2p5/1PKPP3/2P2P2/8/8 w - - 0 0"
STARTINGPOS = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - - 0 0"



def benchmark_zuggenerator():
    """
    Benchmarks the Zuggenerator.
    """

    middle_board = ut.Board(MIDDLEGAME)
    end_board = ut.Board(ENDGAME)
    start_board = ut.Board(STARTINGPOS)

    start_t = time.perf_counter()

    # benchmark start, middle and endgame combined
    for _ in range(1000):
     generate(middle_board)
     generate(end_board)
     generate(start_board)

    end_t = time.perf_counter()

    # benchmark the start position
    start_t_start = time.perf_counter()
    for _ in range(1000):
     generate(start_board)
    end_t_start = time.perf_counter()

    # benchmark the middlegame
    start_t_middle = time.perf_counter()
    for _ in range(1000):
     generate(middle_board)
    end_t_middle = time.perf_counter()

    # benchmark the endgame
    start_t_end = time.perf_counter()
    for _ in range(1000):
     generate(end_board)
    end_t_end = time.perf_counter()

    time_combined = (end_t - start_t)
    time_start = (end_t_start - start_t_start)
    time_middle = (end_t_middle - start_t_middle)
    time_end = (end_t_end - start_t_end)

    print("\n    --------------- Results of Zuggenerator Benchmark ---------------")
    print("")
    print(f"    Benchmark of combination of start-, mid- and endgame:   {time_combined} seconds ")
    print(f"    Benchmark of Starting position:                         {time_start} seconds")
    print(f"    Benchmark of middlegame:                                {time_middle} seconds")
    print(f"    Benchmark of endgame:                                   {time_end} seconds")


# def benchmark_alpha_beta(time_limit = 120):
#     print("-----    ALPHA-BETA BENCHMARK    -----")
#     fen_1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
#     fen_2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"

#     board_1 = zg.Board(fen_1)
#     board_2 = zg.Board(fen_2)

#     print("Stellung 1")
#     zg.iterative_deepening_alpha_beta_search(board_1, 100, time_limit)
#     print("Stellung 2")
#     zg.iterative_deepening_alpha_beta_search(board_2, 100, time_limit)

# def benchmark_minimax(time_limit = 120):
#     print("-----    MINIMAX BENCHMARK    -----")
#     fen_1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
#     fen_2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"

#     board_1 = zg.Board(fen_1)
#     board_2 = zg.Board(fen_2)

#     print("Stellung 1")
#     zg.minimax(board_1, 100, time_limit)
#     print("Stellung 2")
#     zg.minimax(board_2, 100, time_limit)


# def benchmark_for_us_minimax_alpha_beta(time_limit = 120):
#     print("-----    ALPHA-BETA BENCHMARK    -----")
#     fen_1 = "3rk1r1/pp3p1p/1nb1p3/8/qn2P2Q/3B1N2/PP3PPP/3R1RK1 w - - 0 1"
#     fen_2 = "4R2Q/3q1p1p/6p1/5k2/8/1pp3P1/p2r1PPK/8 w - - 0 1"
#     fen_3 = "r2qr1k1/p4ppp/2Q1b3/4N3/5B2/3BnP2/PP4PP/R4RK1 w - - 0 19" # stellung gruppe V
#     fen_4 = ""

#     board_1 = zg.Board(fen_1)
#     board_2 = zg.Board(fen_2)
#     board_3 = zg.Board(fen_3)

#     print("Problemstellung 1")
#     zg.iterative_deepening_alpha_beta_search(board_1, 100, time_limit)
#     print("Problemstellung 2")
#     zg.iterative_deepening_alpha_beta_search(board_2, 100, time_limit)
#     print("Gruppe V str 1")
#     zg.iterative_deepening_alpha_beta_search(board_3, 100, time_limit)

#     print("-----    MINIMAX BENCHMARK    -----")

#     board_1 = zg.Board(fen_1)
#     board_2 = zg.Board(fen_2)

#     print("Problemstellung 1")
#     zg.minimax(board_1, 100, time_limit)
#     print("Problemstellung 2")
#     zg.minimax(board_2, 100, time_limit)
#     print("Gruppe V str 1")
#     zg.minimax(board_3, 100, time_limit)

def benchmark_mts3(time_limit = 2):
    print("-----    ALPHA-BETA BENCHMARK    -----")
    fen_1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    fen_2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"

    board_1 = ut.Board(fen_1)
    board_2 = ut.Board(fen_2)

    print("-----    Alpha-Beta    -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_search(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_search(board_2, time_limit)

    print("----- Transposition Tables -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_TT(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_TT(board_2, time_limit)

    print("-----   Alpha-Beta sorting   -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_sorted(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_sorted(board_2, time_limit)

    print("----   PVS  ----")
    print("Problemstellung 1")
    pvs(board_1, time_limit)
    print("Problemstellung 2")
    pvs(board_2, time_limit)

    print("----  MCTS  ----")
    print("Problemstellung 1")
    mcts(board_1, time_limit)
    print("Problemstellung 2")
    mcts(board_2, time_limit)

    #print("----- Alpha-Beta sorting + Transposition Tables -----")
    #print("Problemstellung 1")
    #iterative_deepening_alpha_beta_Sorted_TT(board_1, time_limit, time_limit)
    #print("Problemstellung 2")
    #iterative_deepening_alpha_beta_Sorted_TT(board_2, time_limit, time_limit)



def benchmarks_mst4(time_limit = 120):
    print("-----    ALPHA-BETA BENCHMARK    -----")
    fen_1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    fen_2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"

    board_1 = ut.Board(fen_1)
    board_2 = ut.Board(fen_2)

    print("----- Alpha-Beta sorting -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_sorted(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_sorted(board_2, time_limit)

    print("----- Alpha-Beta TT -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_TT(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_TT(board_2, time_limit)

    print("----- MCTS -----")
    print("Problemstellung 1")
    mcts(board_1, time_limit)
    print("Problemstellung 2")
    mcts(board_2, time_limit)

    print("-----    PVS    -----")
    print("Problemstellung 1")
    pvs(board_1, time_limit)
    print("Problemstellung 2")
    pvs(board_2, time_limit)

    print("-----   PVS sorting   -----")
    print("Problemstellung 1")
    pvs_sort(board_1, time_limit)
    print("Problemstellung 2")
    pvs_sort(board_2, time_limit)

    print("----- PVS Multiprocessing -----")
    print("Problemstellung 1")
    pvs_multi(board_1, time_limit)
    print("Problemstellung 2")
    pvs_multi(board_2, time_limit)

    print("----   PVS MP sorting  ----")
    print("Problemstellung 1")
    pvs_multi_sort(board_1, time_limit)
    print("Problemstellung 2")
    pvs_multi_sort(board_2, time_limit)

    print("----   PVS sorting qs  ----")
    print("Problemstellung 1")
    pvs_sort_qs(board_1, time_limit)
    print("Problemstellung 2")
    pvs_sort_qs(board_2, time_limit)

    print("----   PVS MP sorting qs  ----")
    print("Problemstellung 1")
    pvs_multi_sort_qs(board_1, time_limit)
    print("Problemstellung 2")
    pvs_multi_sort_qs(board_2, time_limit)


def extra_benchmarks_dev(time_limit=120):
    print("-----    ALPHA-BETA BENCHMARK    -----")
    fen_1 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    fen_2 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"

    board_1 = ut.Board(fen_1)
    board_2 = ut.Board(fen_2)

    print("----- Alpha-Beta TT -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_TT(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_TT(board_2, time_limit)

    print("-----    Alpha-Beta    -----")
    print("Problemstellung 1")
    iterative_deepening_alpha_beta_search(board_1, time_limit)
    print("Problemstellung 2")
    iterative_deepening_alpha_beta_search(board_2, time_limit)



if __name__ == "__main__":
    gen_all_masks()
    #benchmark_zuggenerator()
    #benchmark_alpha_beta()
    #benchmark_minimax()
    #benchmark_for_us_minimax_alpha_beta()
    #benchmark_mts3()
    benchmarks_mst4(1)
    extra_benchmarks_dev(1)
    benchmark_zuggenerator()
