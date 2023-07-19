import sys

from core.zuggenerator import gen_all_masks
from core.utils import Board, Move
from core.aitech.pvs.pvs_sorted_multi_qs import pvs_multi_sort_qs

def get_move(board: Board, time_limit: int) -> Move:
    move = pvs_multi_sort_qs(board=board, time_limit=time_limit)
    return move


def main():
    args = sys.argv[1:]

    fen = ""
    time_limit = 7
    all = False
    for i, arg in enumerate(args):
        if arg == "-fen":
            if len(args) < i + 2:
                print("No fen was specified. Abort")
                return
            fen = args[i + 1: i + 7]
        elif arg == "-a":
            all = True
        elif arg == "-t":
            if len(args) < i + 2:
                print("No time was specified. Abort")
                return
            time_limit = args[i + 1]
        else:
            pass

    try:
        time_limit = int(time_limit)
    except Exception as e:
        print("time invalid. Must be int. Abort")
        return

    if fen == "":
        print("No fen was provided. Abort")
        return
    fen = " ".join(fen)

    try:
        board = Board(fen)
    except Exception as e:
        print("fen was invalid. Abort")
        return

    move = get_move(board, time_limit = time_limit)
    print(f"Best move: {move}")





if __name__ == "__main__":
    gen_all_masks()
    main()
