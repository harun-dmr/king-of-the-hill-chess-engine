"""

Alpha-Beta pruning with Transposition Table using zobrist Hashing

"""
import random
import time
import copy
import numpy as np

from core.utils import Board, Move
from core.zuggenerator import generate, game_ending, gen_all_masks, lsb_generator, sort_moves
from core.eval import evaluate_board


rank_8 = 0xFF
rank_7 = 0xFF00
rank_6 = 0xFF0000
rank_5 = 0xFF000000
rank_4 = 0xFF00000000
rank_3 = 0xFF0000000000
rank_2 = 0xFF000000000000
rank_1 = 0xFF00000000000000

a_file = 0x0101010101010101
b_file = 0x0202020202020202
c_file = 0x0404040404040404
d_file = 0x0808080808080808
e_file = 0x1010101010101010
f_file = 0x2020202020202020
g_file = 0x4040404040404040
h_file = 0x8080808080808080

white_king = 0x1000000000000000
black_king = 0x10

a_1 = 0x100000000000000
h_1 = 0x8000000000000000
a_8 = 0x1
h_8 = 0x80

center = 0x0000001818000000




ZOBRIST_PIECES = [{} for _ in range(12)]
ZOBRIST_PIECES_ARR = np.zeros((64, 12))
BLACK_TO_MOVE = 0
ZOBRIST_CASTLING = {}


def init_zobrist():
    pos = 1
    for i in range(65):
        for j in range(12):
            random_number = random.getrandbits(64)
            while random_number in ZOBRIST_PIECES[j].values():
                random_number = random.getrandbits(64)
            ZOBRIST_PIECES[j][pos] = random_number

        pos <<= 1

    random_number = random.getrandbits(64)
    while random_number in ZOBRIST_PIECES:
        random_number = random.getrandbits(64)
    BLACK_TO_MOVE = random_number

    # castling
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    random_number = random.getrandbits(64)
                    while random_number in ZOBRIST_PIECES:
                        random_number = random.getrandbits(64)
                    ZOBRIST_CASTLING[(bool(i), bool(j), bool(k), bool(l))] = random_number

init_zobrist()



class BoardZobrist(Board):
    def __init__(self, board: Board=None, fen=None):
        super(BoardZobrist, self).__init__(fen)

        if board is not None:
            self.boards = board.boards
            self.castling_bk = board.castling_bk
            self.castling_bq = board.castling_bq
            self.castling_wk = board.castling_wk
            self.castling_wq = board.castling_wq
            self.active_color = board.active_color
            self.moves = board.moves
            self.init_zobrist()

        self.zobrist: int
        if fen is not None:
            self.init_zobrist()

    def init_zobrist(self):
        zkey = 0
        if not self.active_color:
            zkey ^= BLACK_TO_MOVE
        for i, mask in enumerate(self.boards[:-2]):
            for pos in lsb_generator(mask):
                zkey ^= ZOBRIST_PIECES[i][pos]

        zkey ^= ZOBRIST_CASTLING[(self.castling_bk,
                                  self.castling_bq,
                                  self.castling_wk,
                                  self.castling_wq)]

        self.zobrist = zkey



    def __deepcopy__(self, memodict={}):
        b = BoardZobrist()
        b.active_color = self.active_color

        b.castling_wq = self.castling_wq
        b.castling_wk = self.castling_wk
        b.castling_bk = self.castling_bk
        b.castling_bq = self.castling_bq
        if self.moves is None:
            b.moves = None
        else:
            b.moves = [move for move in self.moves]

        b.zobrist = self.zobrist

        b.boards = [x for x in self.boards]

        return b


    def do_move(self, move: Move):
        """
        Changes Bitboards acording to Move.
        Changes active color.

        :param move: The move to be executed
        :return: nothing
        """

        prom_trans = {
            2: 4,
            3: 3,
            4: 1,
            5: 2,
            8: 4,
            9: 3,
            10: 1,
            11: 2
        }

        nbitboard = {
            2: [self.black_pieces, self.queens],
            3: [self.black_pieces, self.rooks],
            4: [self.black_pieces, self.knights],
            5: [self.black_pieces, self.bishops],

            8: [self.white_pieces, self.queens],
            9: [self.white_pieces, self.rooks],
            10: [self.white_pieces, self.knights],
            11: [self.white_pieces, self.bishops]
        }

        # zobrist
        self.zobrist ^= BLACK_TO_MOVE

        # pawn promotion --> set bitboards of new piece
        if move.promotion is not None:
            self.zobrist ^= ZOBRIST_PIECES[0][move.origin]
            # change bitboards of captured piece
            if move.capture is not None:
                for i in range(len(self.boards)):
                    if self.boards[i] & move.target:
                        self.boards[i] = self.boards[i] & ~move.target
                        # zobrist
                        ZOBRIST_PIECES[i][move.target]
            nbitboard.get(move.promotion)[0] = nbitboard.get(move.promotion)[0] | move.target
            nbitboard.get(move.promotion)[1] = nbitboard.get(move.promotion)[1] | move.target
            # change bitboards of moved piece
            for i in range(len(self.boards)):
                if self.boards[i] & move.origin:
                    self.boards[i] = self.boards[i] & ~move.origin
            # change turns
            self.active_color = not self.active_color
            # zobrist
            self.zobrist ^= ZOBRIST_PIECES[prom_trans[move.promotion]][move.target]
            return
        elif move.castle is not None:
            # zobrist
            # kings
            # self.zobrist ^= ZOBRIST_PIECES[5][move.origin]
            # self.zobrist ^= ZOBRIST_PIECES[5][move.target]
            # rooks
            self.zobrist ^= ZOBRIST_PIECES[3][move.castle.origin]
            self.zobrist ^= ZOBRIST_PIECES[3][move.castle.target]

            self.zobrist ^= ZOBRIST_CASTLING[(self.castling_bk,
                                              self.castling_bq,
                                              self.castling_wk,
                                              self.castling_wq)]

            # change bitboards of castled rook
            for i in range(len(self.boards)):
                if self.boards[i] & move.castle.origin:
                    self.boards[i] = self.boards[i] & ~move.castle.origin
                    self.boards[i] = self.boards[i] | move.castle.target
            if move.origin == white_king:
                self.castling_wk = False
                self.castling_wq = False
            else:
                self.castling_bk = False
                self.castling_bq = False

        # remove castling rights if king gets moved
        elif move.origin == black_king:
            self.castling_bk = False
            self.castling_bq = False
        elif move.origin == white_king:
            self.castling_wk = False
            self.castling_wq = False
        # remove castling rights if rook gets moved
        elif move.origin == a_8:
            self.castling_bq = False
        elif move.origin == h_8:
            self.castling_bk = False
        elif move.origin == a_1:
            self.castling_wq = False
        elif move.origin == h_1:
            self.castling_wk = False

        # remove castling rights if rook gets taken
        if move.target == a_8:
            self.castling_bq = False
        elif move.target == h_8:
            self.castling_bk = False
        elif move.target == a_1:
            self.castling_wq = False
        elif move.target == h_1:
            self.castling_wk = False

        # change bitboards of captured piece
        if move.capture is not None:
            for i in range(len(self.boards)):
                if self.boards[i] & move.target:
                    self.boards[i] = self.boards[i] & ~move.target
                    # zobrist
                    self.zobrist ^= ZOBRIST_PIECES[i][move.target]

        # change bitboards of moved piece
        for i in range(len(self.boards)):
            if self.boards[i] & move.origin:
                self.boards[i] = self.boards[i] & ~move.origin
                self.boards[i] = self.boards[i] | move.target
                # zobrist
                self.zobrist ^= ZOBRIST_PIECES[i][move.origin]
                self.zobrist ^= ZOBRIST_PIECES[i][move.target]

        # change turns
        self.active_color = not self.active_color
        self.moves = None

        # zobrist
        self.zobrist ^= ZOBRIST_CASTLING[(self.castling_bk,
                                          self.castling_bq,
                                          self.castling_wk,
                                          self.castling_wq)]



class MoveChooserTT:

    def __init__(self):
        self.transposition_table = {}

    def alpha_beta(self, board: BoardZobrist, depth: int, alpha: float, beta: float, stop_time: float, move: Move = None) -> (
    float, Move, int):
        # if depth == 0 or game_ending(board):
        #     return eval_move(board, move), None

        trans = self.transposition_table.get(board.zobrist)

        if trans is not None:
            if trans[2] >= depth:
                return trans[0], trans[1], 1

        best_move = None
        moves = generate(board)
        #moves = sort_moves(moves)

        # Sort Moves using Transposition Table as a heuristic

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
                    score, _, z = self.alpha_beta(board_copy, depth - 1, alpha, beta, stop_time)
                    zuege += z

                if score > max_score:
                    max_score = score
                    best_move = move

                alpha = max(alpha, max_score)
                if alpha >= beta:
                    break

            self.transposition_table[board] = (max_score, best_move, depth)
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
                    score, _, z = self.alpha_beta(board_copy, depth - 1, alpha, beta, stop_time)
                    zuege += z

                if score < min_score:
                    min_score = score
                    best_move = move

                beta = min(beta, min_score)
                if alpha >= beta:
                    break

            self.transposition_table[board.zobrist] = (min_score, best_move, depth)
            return min_score, best_move, zuege

    def sort(self, board, moves):
        sorted_moves = []
        unsorted_moves = []
        best_move = None

        transposition_entry = self.transposition_table.get(board)
        if transposition_entry:
            score, best_move, depth = transposition_entry

        for move in moves:
            if move == best_move:
                sorted_moves.insert(0, move)  # Put the best move at the beginning
            else:
                temp_board = copy.deepcopy(board)
                temp_board.do_move(move)
                unsorted_moves.append(move)

        def key_alpha_beta_sorted(move: Move):
            b = copy.deepcopy(board)
            b.do_move(move)
            trans = self.transposition_table.get(b)
            if trans is not None:
                return trans[0]
            return 0

        if not board.active_color:
            unsorted_moves.sort(key=key_alpha_beta_sorted)
        else:
            unsorted_moves.sort(key=key_alpha_beta_sorted, reverse=True)
        sorted_moves.extend(unsorted_moves)
        return sorted_moves


def iterative_deepening_alpha_beta_TT(board: Board, time_limit: float) -> Move:
    board = BoardZobrist(board=board)

    best_move = None
    max_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    stop_time = time.time() + time_limit
    depth = 1

    mc = MoveChooserTT()

    while time.time() < stop_time:
        t1 = time.time()
        score, move, zustaende = mc.alpha_beta(board, depth, alpha, beta, stop_time)
        t2 = time.time()
        if score > max_score and time.time() < stop_time:
            max_score = score
            best_move = move
        if best_move is not None:
            print(f"depth: {depth},     time: {round(t2 - t1, 4)}s,   zustände: {zustaende}")
        depth += 1

    return best_move



if __name__ == "__main__":
    gen_all_masks()
    print(max(ZOBRIST_PIECES[3]))
    print(18446744073709551616 in ZOBRIST_PIECES[3])
    fen1 = "r4rk1/1bp1qp1p/p2p1np1/2nPp3/2P1P3/1PN2N2/PB1Q1PPP/R3K2R w KQ - 2 14"
    fen2 = "r2q1rk1/pp2ppbp/2np1np1/8/2PP4/2N1PN2/PPQ2PPP/R1B1K2R b KQ - 4 8"
    board_1 = BoardZobrist(fen=fen1)
    iterative_deepening_alpha_beta_TT(board_1, 7, 120)
    board_2 = BoardZobrist(fen=fen2)
    iterative_deepening_alpha_beta_TT(board_2, 7, 120)
    #print(board_1.zobrist)