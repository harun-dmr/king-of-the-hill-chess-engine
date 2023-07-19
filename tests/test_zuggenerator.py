from context import Board, Move
from context import pawn_moves, pawn_moves_pos, knight_moves, bishops_moves, queen_moves, king_moves, rooks_moves, rook_moves, gen_all_masks, generate, all_moves
from context import print_bitboards, print_bitboard

a1 = 72057594037927936
a2 = 281474976710656
a3 = 1099511627776
a4 = 4294967296
a5 = 16777216
a6 = 65536
a7 = 256
a8 = 1
b1 = 144115188075855872
b2 = 562949953421312
b3 = 2199023255552
b4 = 8589934592
b5 = 33554432
b6 = 131072
b7 = 512
b8 = 2
c1 = 288230376151711744
c2 = 1125899906842624
c3 = 4398046511104
c4 = 17179869184
c5 = 67108864
c6 = 262144
c7 = 1024
c8 = 4
d1 = 576460752303423488
d2 = 2251799813685248
d3 = 8796093022208
d4 = 34359738368
d5 = 134217728
d6 = 524288
d7 = 2048
d8 = 8
e1 = 1152921504606846976
e2 = 4503599627370496
e3 = 17592186044416
e4 = 68719476736
e5 = 268435456
e6 = 1048576
e7 = 4096
e8 = 16
f1 = 2305843009213693952
f2 = 9007199254740992
f3 = 35184372088832
f4 = 137438953472
f5 = 536870912
f6 = 2097152
f7 = 8192
f8 = 32
g1 = 4611686018427387904
g2 = 18014398509481984
g3 = 70368744177664
g4 = 274877906944
g5 = 1073741824
g6 = 4194304
g7 = 16384
g8 = 64
h1 = 9223372036854775808
h2 = 36028797018963968
h3 = 140737488355328
h4 = 549755813888
h5 = 2147483648
h6 = 8388608
h7 = 32768
h8 = 128

import unittest


class PawnMovesPosTests(unittest.TestCase):
    def test_starting_position_middle(self):
        board = Board()

        board.active_color = True
        board.castling_bk = True
        board.castling_bq = True
        board.castling_wk = True
        board.castling_wq = True
        board.boards = [71776119061282560, 4755801206503243842, 2594073385365405732, 9295429630892703873,
                        576460752303423496, 1152921504606846992, 65535, 18446462598732840960]

        expected_moves = {
            Move(origin=0x8000000000000, target=0x800000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x8000000000000, target=0x80000000000, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves_pos(board, pos=2251799813685248))

        self.assertSetEqual(moves, expected_moves)

    def test_starting_position_a_file(self):
        board = Board()

        board.active_color = True
        board.castling_bk = True
        board.castling_bq = True
        board.castling_wk = True
        board.castling_wq = True
        board.boards = [71776119061282560, 4755801206503243842, 2594073385365405732, 9295429630892703873,
                        576460752303423496, 1152921504606846992, 65535, 18446462598732840960]

        expected_moves = {
            Move(origin=281474976710656, target=1099511627776, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=281474976710656, target=4294967296, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves_pos(board, pos=281474976710656))

        self.assertSetEqual(moves, expected_moves)

    def test_starting_position_h_file(self):
        board = Board()

        board.active_color = True
        board.castling_bk = True
        board.castling_bq = True
        board.castling_wk = True
        board.castling_wq = True
        board.boards = [71776119061282560, 4755801206503243842, 2594073385365405732, 9295429630892703873,
                        576460752303423496, 1152921504606846992, 65535, 18446462598732840960]

        expected_moves = {
            Move(origin=36028797018963968, target=140737488355328, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=36028797018963968, target=549755813888, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves_pos(board, pos=36028797018963968))

        self.assertSetEqual(moves, expected_moves)

    def test_capture_middle_left_attack(self):
        # fen = "1k6/4p2r/5P2/8/8/8/2R5/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [2101248, 0, 0, 1125899906875392, 0, 576460752303423490, 36866, 577586652212363264]

        expected_moves = {Move(origin=2097152, target=8192, capture=False, promotion=None, castle=None, piece=1),
                          Move(origin=2097152, target=4096, capture=True, promotion=None, castle=None, piece=1)}

        moves = set(pawn_moves_pos(board, pos=2097152))

        self.assertSetEqual(moves, expected_moves)

    def test_capture_middle_right_attack(self):
        # fen = "1k6/6pr/5P2/8/8/8/2R5/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [2113536, 0, 0, 1125899906875392, 0, 576460752303423490, 49154, 577586652212363264]

        expected_moves = {Move(origin=2097152, target=8192, capture=False, promotion=None, castle=None, piece=1),
                          Move(origin=2097152, target=16384, capture=True, promotion=None, castle=None, piece=1)}

        moves = set(pawn_moves_pos(board, pos=2097152))

        self.assertSetEqual(moves, expected_moves)

    def test_capture_middle_left_and_right_attack(self):
        # fen = "1k6/4p1pr/5P2/8/8/8/2R5/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [2117632, 0, 0, 1125899906875392, 0, 576460752303423490, 53250, 577586652212363264]

        expected_moves = {Move(origin=2097152, target=8192, capture=False, promotion=None, castle=None, piece=1),
                          Move(origin=2097152, target=16384, capture=True, promotion=None, castle=None, piece=1),
                          Move(origin=2097152, target=4096, capture=True, promotion=None, castle=None, piece=1)}

        moves = set(pawn_moves_pos(board, pos=2097152))

        self.assertSetEqual(moves, expected_moves)

    def test_capture_a_file(self):
        # fen = "1k4r1/1p5p/P7/8/8/8/2R5/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [98816, 0, 0, 1125899906842688, 0, 576460752303423490, 33346, 577586652210331648]

        expected_moves = {Move(origin=65536, target=256, capture=False, promotion=None, castle=None, piece=1),
                          Move(origin=65536, target=512, capture=True, promotion=None, castle=None, piece=1)}

        moves = set(pawn_moves_pos(board, pos=65536))

        self.assertSetEqual(moves, expected_moves)

    def test_capture_h_file(self):
        # fen = "1k4r1/p5p1/7P/8/8/8/2R5/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [8405248, 0, 0, 1125899906842688, 0, 576460752303423490, 16706, 577586652218654720]

        expected_moves = {Move(origin=8388608, target=32768, capture=False, promotion=None, castle=None, piece=1),
                          Move(origin=8388608, target=16384, capture=True, promotion=None, castle=None, piece=1)}

        moves = set(pawn_moves_pos(board, pos=8388608))

        self.assertSetEqual(moves, expected_moves)

    def test_blocked_no_attack(self):
        # fen = "1k6/8/2p1p1p1/4P3/8/8/8/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [273940480, 0, 0, 0, 0, 576460752303423490, 5505026, 576460752571858944]

        expected_moves = []

        moves = set(pawn_moves_pos(board, pos=268435456))

        self.assertSetEqual(moves, set(expected_moves))

    def test_blocked_attack(self):
        # fen = "1k6/8/3ppp2/4P3/8/8/8/3K4 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [272105472, 0, 0, 0, 0, 576460752303423490, 3670018, 576460752571858944]

        expected_moves = {Move(origin=268435456, target=2097152, capture=True, promotion=None, castle=None, piece=1),
                          Move(origin=268435456, target=524288, capture=True, promotion=None, castle=None, piece=1)}

        moves = set(pawn_moves_pos(board, pos=268435456))

        self.assertSetEqual(moves, expected_moves)

    def test_promotion_white(self):
        # fen = "4r3/1q3P2/2k5/8/8/1R6/2K2p2/4R3 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [9007199254749184, 0, 0, 1152923703630102544, 512, 1125899907104768, 9007199255003664,
                        1154049603536953344]

        expected_moves = {
            Move(origin=0x2000, target=0x20, capture=False, promotion=8, castle=None, piece=1),
            Move(origin=0x2000, target=0x20, capture=False, promotion=9, castle=None, piece=1),
            Move(origin=0x2000, target=0x20, capture=False, promotion=10, castle=None, piece=1),
            Move(origin=0x2000, target=0x20, capture=False, promotion=11, castle=None, piece=1),
            Move(origin=0x2000, target=0x10, capture=True, promotion=8, castle=None, piece=1),
            Move(origin=0x2000, target=0x10, capture=True, promotion=9, castle=None, piece=1),
            Move(origin=0x2000, target=0x10, capture=True, promotion=10, castle=None, piece=1),
            Move(origin=0x2000, target=0x10, capture=True, promotion=11, castle=None, piece=1)
        }

        moves = set(pawn_moves_pos(board, pos=0x2000))

        self.assertSetEqual(moves, expected_moves)

    def test_promotion_black(self):
        # fen = "4r3/1q3P2/2k5/8/8/1R6/2K2p2/4R3 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [9007199254749184, 0, 0, 1152923703630102544, 512, 1125899907104768, 9007199255003664,
                        1154049603536953344]

        expected_moves = {
            Move(origin=9007199254740992, target=2305843009213693952, capture=False, promotion=2, castle=None, piece=1),
            Move(origin=9007199254740992, target=2305843009213693952, capture=False, promotion=3, castle=None, piece=1),
            Move(origin=9007199254740992, target=2305843009213693952, capture=False, promotion=4, castle=None, piece=1),
            Move(origin=9007199254740992, target=2305843009213693952, capture=False, promotion=5, castle=None, piece=1),
            Move(origin=9007199254740992, target=1152921504606846976, capture=True, promotion=2, castle=None, piece=1),
            Move(origin=9007199254740992, target=1152921504606846976, capture=True, promotion=3, castle=None, piece=1),
            Move(origin=9007199254740992, target=1152921504606846976, capture=True, promotion=4, castle=None, piece=1),
            Move(origin=9007199254740992, target=1152921504606846976, capture=True, promotion=5, castle=None, piece=1)
        }

        moves = set(pawn_moves_pos(board, pos=9007199254740992))

        self.assertSetEqual(moves, expected_moves)


class PawnMovesTests(unittest.TestCase):

    def test_starting_position_middle(self):
        board = Board()

        board.active_color = True
        board.castling_bk = True
        board.castling_bq = True
        board.castling_wk = True
        board.castling_wq = True
        board.boards = [71776119061282560, 4755801206503243842, 2594073385365405732, 9295429630892703873,
                        576460752303423496, 1152921504606846992, 65535, 18446462598732840960]

        expected_moves = {
            Move(origin=a2, target=a3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=b2, target=b3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=c2, target=c3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d2, target=d3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=e2, target=e3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=f2, target=f3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=g2, target=g3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=h2, target=h3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=a2, target=a4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=b2, target=b4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=c2, target=c4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d2, target=d4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=e2, target=e4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=f2, target=f4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=g2, target=g4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=h2, target=h4, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_middle_game(self):
        # fen = "r1bq1rk1/pppp1ppp/2n1pn2/2b5/2BPP3/2P2N2/PP3PPP/R1BQ1RK1 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [63899320840154880, 35184374448128, 288230393398689796, 2377900603251621921, 576460752303423496,
                        4611686018427387968, 70578029, 7918212272525148160]

        expected_moves = {
            Move(origin=a2, target=a3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=b2, target=b3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d4, target=d5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=e4, target=e5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=g2, target=g3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=h2, target=h3, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=a2, target=a4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=b2, target=b4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d4, target=c5, capture=True, promotion=None, castle=None, piece=1),
            Move(origin=g2, target=g4, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=h2, target=h4, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_middle_game_2(self):
        # fen = "B2R1n2/rQ4P1/1P2PR1B/3p2Kb/k7/pN6/4r3/8 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [1099647041536, 2199023255584, 2155872257, 4503599629467912, 512, 5368709120, 4504705715667232,
                        2200108679689]

        expected_moves = {
            Move(origin=b6, target=a7, capture=True, promotion=None, castle=None, piece=1),
            Move(origin=e6, target=e7, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=g7, target=g8, capture=False, promotion=8, castle=None, piece=1),
            Move(origin=g7, target=g8, capture=False, promotion=9, castle=None, piece=1),
            Move(origin=g7, target=g8, capture=False, promotion=10, castle=None, piece=1),
            Move(origin=g7, target=g8, capture=False, promotion=11, castle=None, piece=1),
            Move(origin=g7, target=f8, capture=True, promotion=8, castle=None, piece=1),
            Move(origin=g7, target=f8, capture=True, promotion=9, castle=None, piece=1),
            Move(origin=g7, target=f8, capture=True, promotion=10, castle=None, piece=1),
            Move(origin=g7, target=f8, capture=True, promotion=11, castle=None, piece=1),
        }

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_middle_game_black(self):
        # fen = "r1bq1rk1/pppp1ppp/2n1pn2/2b5/2BPP3/2P2N2/PP3PPP/R1BQ1RK1 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [63899320840154880, 35184374448128, 288230393398689796, 2377900603251621921, 576460752303423496,
                        4611686018427387968, 70578029, 7918212272525148160]

        expected_moves = {
            Move(origin=a7, target=a6, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=a7, target=a5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=b7, target=b6, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=b7, target=b5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d7, target=d6, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d7, target=d5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=e6, target=e5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=g7, target=g6, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=g7, target=g5, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=h7, target=h6, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=h7, target=h5, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_middle_game_2_black(self):
        # fen = "B2R1n2/rQ4P1/1P2PR1B/3p2Kb/k7/pN6/4r3/8 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [1099647041536, 2199023255584, 2155872257, 4503599629467912, 512, 5368709120, 4504705715667232,
                        2200108679689]

        expected_moves = {
            Move(origin=a3, target=a2, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=d5, target=d4, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_blocked_white(self):
        # fen = "3k4/8/8/p1p2p1p/P1P2P1P/8/8/4K3 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [711437844480, 0, 0, 0, 0, 1152921504606846984, 2768240648, 1152922213276450816]

        expected_moves = []

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, set(expected_moves))

    def test_blocked_black(self):
        # fen = "3k4/8/8/p1p2p1p/P1P2P1P/8/8/4K3 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [711437844480, 0, 0, 0, 0, 1152921504606846984, 2768240648, 1152922213276450816]

        expected_moves = []

        moves = set(pawn_moves(board))

        self.assertSetEqual(moves, set(expected_moves))


class KnightMovesTests(unittest.TestCase):
    def setUp(self) -> None:
        gen_all_masks()
    def test_fen_1(self):
        # fen = "2B2K2/4P2r/6q1/2PpPR2/Q6n/p1pp4/6P1/6k1 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [18028692630409216, 549755813888, 4, 536903680, 4299161600, 4611686018427387936,
                        4611700861972807680, 18014403676868644]

        expected_moves = {
            Move(origin=h4, target=f5, capture=True, promotion=None, castle=None, piece=2),
            Move(origin=h4, target=f3, capture=False, promotion=None, castle=None, piece=2),
            Move(origin=h4, target=g2, capture=True, promotion=None, castle=None, piece=2)
        }

        moves = set(knight_moves(board))

        self.assertSetEqual(moves, expected_moves)


class BishopMovesTests(unittest.TestCase):
    def test_fen_1(self):
        # fen = "1k6/p1nrp3/n2p4/2p5/3PP3/2P2P2/P7/BN4K1 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [321160542163200, 144115188075922432, 72057594037927936, 2048, 0, 4611686018427387906, 67706114,
                        4828179961015697408]

        expected_moves = {
            Move(origin=a1, target=b2, capture=False, promotion=None, castle=None, piece=3)
        }
        moves = set(bishops_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_fen_2(self):
        # fen = "8/3np3/3pk3/2p5/1PKPP3/2P2P2/8/8 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [39694155386880, 2048, 0, 0, 0, 17180917760, 68687872, 39711267618816]

        expected_moves = []
        moves = bishops_moves(board)

        self.assertListEqual(moves, expected_moves)

    def test_fen_3(self):
        # fen = "8/3k4/6R1/1N2b3/8/8/8/1K6 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [0, 33554432, 268435456, 4194304, 0, 144115188075857920, 268437504, 144115188113604608]

        expected_moves = {
            Move(origin=e5, target=a1, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=b2, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=c3, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=d4, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=f6, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=g7, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=h8, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=f4, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=g3, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=h2, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=d6, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=c7, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=b8, capture=False, promotion=None, castle=None, piece=3)
        }

        moves = set(bishops_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_attack(self):
        # fen = "8/3k2P1/3P2R1/1N2b3/3P1P2/8/8/1K6 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [171799232512, 33554432, 268435456, 4194304, 0, 144115188075857920, 268437504,
                        144115359912837120]

        expected_moves = {
            Move(origin=e5, target=d4, capture=True, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=f6, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=g7, capture=True, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=f4, capture=True, promotion=None, castle=None, piece=3),
            Move(origin=e5, target=d6, capture=True, promotion=None, castle=None, piece=3)
        }

        moves = set(bishops_moves(board))

        self.assertSetEqual(moves, expected_moves)


class QueenMovesTests(unittest.TestCase):
    def test_fen_1(self):
        # fen = "1k6/p1nrp3/n2p4/2p5/3PP3/2P2P2/P7/QN4K1 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [321160542163200, 144115188075922432, 0, 2048, 72057594037927936, 4611686018427387906, 67706114,
                        4828179961015697408]

        expected_moves = {
            Move(origin=a1, target=b2, capture=False, promotion=None, castle=None, piece=6)
        }
        moves = set(queen_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_fen_2(self):
        # fen = "8/3np3/3pk3/2p5/1PKPP3/2P2P2/8/8 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [39694155386880, 2048, 0, 0, 0, 17180917760, 68687872, 39711267618816]

        expected_moves = []
        moves = queen_moves(board)

        self.assertListEqual(moves, expected_moves)
    def test_fen_3(self):
        # fen = "8/3k4/6R1/1N2q3/8/8/8/1K6 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [0, 33554432, 0, 4194304, 268435456, 144115188075857920, 268437504, 144115188113604608]

        expected_moves = {
            Move(origin=e5, target=a1, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=b2, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=c3, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=d4, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=f6, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=g7, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=h8, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=f4, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=g3, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=h2, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=d6, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=c7, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=b8, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e4, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e3, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e2, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e1, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e6, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e7, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=e8, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=d5, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=c5, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=b5, capture=True, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=f5, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=g5, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=e5, target=h5, capture=False, promotion=None, castle=None, piece=6)
        }

        moves = set(queen_moves(board))

        self.assertSetEqual(moves, expected_moves)


class KingMovesTests(unittest.TestCase):
    def test_fen_1(self):
        # fen = "1k6/p1nrp3/n2p4/2p5/3PP3/2P2P2/P7/RN4K1 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [321160542163200, 144115188075922432, 0, 72057594037929984, 0, 4611686018427387906, 67706114,
                        4828179961015697408]

        expected_moves = {
            Move(origin=g1, target=f1, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=g1, target=h1, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=g1, target=f2, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=g1, target=g2, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=g1, target=h2, capture=False, promotion=None, castle=None, piece=7),
        }

        moves = set(king_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_fen_2(self):
        # fen = "8/3np3/3pk3/2p5/1PKPP3/2P2P2/8/8 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [39694155386880, 2048, 0, 0, 0, 17180917760, 68687872, 39711267618816]

        expected_moves = {
            Move(origin=c4, target=b3, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=c4, target=d3, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=c4, target=b5, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=c4, target=c5, capture=True, promotion=None, castle=None, piece=7),
            Move(origin=c4, target=d5, capture=False, promotion=None, castle=None, piece=7),
        }

        moves = set(king_moves(board))

        self.assertSetEqual(moves, expected_moves)


    def test_boxed(self):
        # fen = "6nk/6pp/8/8/8/8/PP6/KN6 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [844424930181120, 144115188075855936, 0, 0, 0, 72057594037928064, 49344, 217017207043915776]

        expected_moves = []
        moves = king_moves(board)

        self.assertListEqual(moves, expected_moves)


class RookMovesTests(unittest.TestCase):

    def test_fen_1(self):
        # fen = "1k6/p1nrp3/n2p4/2p5/3PP3/2P2P2/P7/RN4K1 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [321160542163200, 144115188075922432, 0, 72057594037929984, 0, 4611686018427387906, 67706114,
                        4828179961015697408]

        expected_moves = []
        moves = rooks_moves(board)

        self.assertListEqual(moves, expected_moves)

    def test_fen_2(self):
        # fen = "8/3np3/3pk3/2p5/1PKPP3/2P2P2/8/8 w - - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [39694155386880, 2048, 0, 0, 0, 17180917760, 68687872, 39711267618816]

        expected_moves = []
        moves = rooks_moves(board)

        self.assertListEqual(moves, expected_moves)

    def test_capture(self):
        # fen = "8/3k4/6R1/1N2r3/8/8/8/1K6 b - - 0 1"
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [0, 33554432, 0, 272629760, 0, 144115188075857920, 268437504, 144115188113604608]

        expected_moves = {
            Move(origin=e5, target=e4, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=e3, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=e2, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=e1, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=e6, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=e7, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=e8, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=d5, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=c5, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=b5, capture=True, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=f5, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=g5, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=e5, target=h5, capture=False, promotion=None, castle=None, piece=5)
        }

        moves = set(rooks_moves(board))

        self.assertSetEqual(moves, expected_moves)

class GenerateMovesTests(unittest.TestCase):
    def setUp(self) -> None:
        gen_all_masks()

    def test_starting_position(self):
        # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = True
        board.castling_bq = True
        board.castling_wk = True
        board.castling_wq = True
        board.boards = [71776119061282560, 4755801206503243842, 2594073385365405732, 9295429630892703873,
                        576460752303423496, 1152921504606846992, 65535, 18446462598732840960]

        expected_moves = {
            Move(origin=0x2000000000000, target=0x20000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x200000000000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=2),
        Move(origin=0x4000000000000, target=0x400000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x2000000000000, target=0x200000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x200000000000000, target=0x40000000000, capture=False, promotion=None, castle=None, piece=2),
        Move(origin=0x40000000000000, target=0x400000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x80000000000000, target=0x8000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x80000000000000, target=0x800000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x4000000000000, target=0x40000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x10000000000000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x1000000000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x10000000000000, target=0x1000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x4000000000000000, target=0x800000000000, capture=False, promotion=None, castle=None, piece=2),
        Move(origin=0x8000000000000, target=0x800000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x20000000000000, target=0x2000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x8000000000000, target=0x80000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x40000000000000, target=0x4000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x20000000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x1000000000000, target=0x100000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x4000000000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=2)

        }

        moves = set(generate(board))

        self.assertSetEqual(moves, expected_moves)

    def test_fen_1(self):
        # fen = 4r3/1n3P1b/1q2p3/Q3np1P/6k1/1pK4R/3p1P2/8 w - - 0 1

        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [11261200777093120, 268435968, 32768, 140737488355344, 16908288, 4672924418048, 2254274521367056,
                        9152336953876480]

        expected_moves = {
            Move(origin=0x800000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x800000000000, target=0x8000000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x1000000, target=0x100000000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x1000000, target=0x100, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x800000000000, target=0x80000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x1000000, target=0x10000000, capture=True, promotion=None, castle=None, piece=6),
        Move(origin=0x1000000, target=0x1, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x800000000000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000, target=0x20, capture=False, promotion=8, castle=None, piece=1),
        Move(origin=0x1000000, target=0x200000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x2000, target=0x20, capture=False, promotion=9, castle=None, piece=1),
        Move(origin=0x1000000, target=0x2000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x40000000000, target=0x2000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x2000, target=0x20, capture=False, promotion=10, castle=None, piece=1),
        Move(origin=0x1000000, target=0x4000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x2000, target=0x10, capture=True, promotion=11, castle=None, piece=1),
        Move(origin=0x800000000000, target=0x400000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000, target=0x20, capture=False, promotion=11, castle=None, piece=1),
        Move(origin=0x1000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x1000000, target=0x1000000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x1000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x1000000, target=0x20000, capture=True, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000, target=0x800000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x20000000000000, target=0x2000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x2000, target=0x10, capture=True, promotion=8, castle=None, piece=1),
        Move(origin=0x1000000, target=0x100000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x2000, target=0x10, capture=True, promotion=9, castle=None, piece=1),
        Move(origin=0x20000000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x40000000000, target=0x8000000000000, capture=True, promotion=None, castle=None, piece=7),
        Move(origin=0x2000, target=0x10, capture=True, promotion=10, castle=None, piece=1),
        Move(origin=0x1000000, target=0x10000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x800000000000, target=0x80000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x800000000000, target=0x8000000000, capture=False, promotion=None, castle=None, piece=5)
        }

        moves = set(generate(board))

        self.assertSetEqual(moves, expected_moves)

    def test_fen_2(self):
        # fen = 8/B7/1b1p1K2/Pr2P1P1/1P5R/3q3p/3r2p1/4k1N1 b - - 0 1

        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [18155145947250688, 4611686018427387904, 131328, 2252349603053568, 8796093022208,
                        1152921504608944128, 1173337236545601536, 4611686578134188288]

        expected_moves = {
            Move(origin=0x80000000000, target=0x400000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x2000000, target=0x10000000, capture=True, promotion=None, castle=None, piece=5),
        Move(origin=0x20000, target=0x8, capture=False, promotion=None, castle=None, piece=3),
        Move(origin=0x20000, target=0x4000000, capture=False, promotion=None, castle=None, piece=3),
        Move(origin=0x80000000000, target=0x800000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000000, target=0x1000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000000, target=0x400000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x2000000, target=0x200000000, capture=True, promotion=None, castle=None, piece=5),
        Move(origin=0x800000000000, target=0x80000000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x8000000000000, target=0x4000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x80000000000, target=0x40000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000000, target=0x20000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x20000, target=0x1000000, capture=True, promotion=None, castle=None, piece=3),
        Move(origin=0x20000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=3),
        Move(origin=0x80000000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000, target=0x8000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x80000000000, target=0x400000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x1000000000000000, target=0x800000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x1000000000000000, target=0x2000000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x80000000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x2000000, target=0x1000000, capture=True, promotion=None, castle=None, piece=5),
        Move(origin=0x20000, target=0x400, capture=False, promotion=None, castle=None, piece=3),
        Move(origin=0x8000000000000, target=0x800000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x20000, target=0x100, capture=True, promotion=None, castle=None, piece=3),
        Move(origin=0x80000000000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x8000000000000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x20000, target=0x800000000, capture=False, promotion=None, castle=None, piece=3),
        Move(origin=0x80000000000, target=0x4000000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x20000, target=0x4000000000000000, capture=True, promotion=None, castle=None, piece=3),
        Move(origin=0x80000000000, target=0x10000000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x8000000000000, target=0x2000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x80000000000, target=0x20000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000000, target=0x2000000000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000000000, target=0x8000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x8000000000000, target=0x1000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000000, target=0x4000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x8000000000000, target=0x10000000000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x1000000000000000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x80000000000, target=0x200000000000000, capture=False, promotion=None, castle=None, piece=6),
        Move(origin=0x80000, target=0x10000000, capture=True, promotion=None, castle=None, piece=1),
        Move(origin=0x20000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=3),
        }

        moves = set(generate(board))

        self.assertSetEqual(moves, expected_moves)


    def test_fen_3(self):
        # fen = 8/B7/3p1K2/Pr2p3/1P3p2/7p/6p1/4k1N1 b - - 0 1

        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [18155282312462336, 4611686018427387904, 256, 33554432, 0, 1152921504608944128,
                        1171076778346151936, 4611686027036197120]

        expected_moves = {
            Move(origin=0x2000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000000, target=0x200, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x1000000000000000, target=0x800000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x1000000000000000, target=0x2000000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x2000000, target=0x20000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000000, target=0x1000000, capture=True, promotion=None, castle=None, piece=5),
        Move(origin=0x2000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x2000000, target=0x2, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x2000000, target=0x4000000, capture=False, promotion=None, castle=None, piece=5),
        Move(origin=0x1000000000000000, target=0x8000000000000, capture=False, promotion=None, castle=None, piece=7),
        Move(origin=0x2000000, target=0x200000000, capture=True, promotion=None, castle=None, piece=5),
        Move(origin=0x80000, target=0x8000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x10000000, target=0x1000000000, capture=False, promotion=None, castle=None, piece=1),
        Move(origin=0x800000000000, target=0x80000000000000, capture=False, promotion=None, castle=None, piece=1),
        }

        moves = set(generate(board))

        self.assertSetEqual(moves, expected_moves)

class AllMovesTests(unittest.TestCase):
    def setUp(self) -> None:
        gen_all_masks()

    def test_starting_position(self):
        # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        board = Board()

        board.active_color = True
        board.castling_bk = True
        board.castling_bq = True
        board.castling_wk = True
        board.castling_wq = True
        board.boards = [71776119061282560, 4755801206503243842, 2594073385365405732, 9295429630892703873,
                        576460752303423496, 1152921504606846992, 65535, 18446462598732840960]

        expected_moves = {
            Move(origin=0x2000000000000, target=0x20000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x200000000000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=2),
            Move(origin=0x4000000000000, target=0x400000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x2000000000000, target=0x200000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x200000000000000, target=0x40000000000, capture=False, promotion=None, castle=None, piece=2),
            Move(origin=0x40000000000000, target=0x400000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x80000000000000, target=0x8000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x80000000000000, target=0x800000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x4000000000000, target=0x40000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x10000000000000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x1000000000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x10000000000000, target=0x1000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x4000000000000000, target=0x800000000000, capture=False, promotion=None, castle=None, piece=2),
            Move(origin=0x8000000000000, target=0x800000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x20000000000000, target=0x2000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x8000000000000, target=0x80000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x40000000000000, target=0x4000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x20000000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x1000000000000, target=0x100000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x4000000000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=2)
            }

        moves = set(all_moves(board))

        self.assertSetEqual(moves, expected_moves)

    def test_fen_1(self):
        # fen = "4r3/1n3P1b/1q2p3/Q3np1P/6k1/1pK4R/3p1P2/8 w - - 0 1"

        board = Board()

        board.active_color = True
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [11261200777093120, 268435968, 32768, 140737488355344, 16908288, 4672924418048, 2254274521367056,
                        9152336953876480]

        expected_moves = {
            Move(origin=0x800000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x40000000000, target=0x400000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x40000000000, target=0x80000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x800000000000, target=0x8000000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x1000000, target=0x100000000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x1000000, target=0x100, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x800000000000, target=0x80000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x1000000, target=0x10000000, capture=True, promotion=None, castle=None, piece=6),
            Move(origin=0x1000000, target=0x1, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x800000000000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000, target=0x20, capture=False, promotion=8, castle=None, piece=1),
            Move(origin=0x1000000, target=0x200000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x2000, target=0x20, capture=False, promotion=9, castle=None, piece=1),
            Move(origin=0x1000000, target=0x2000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x40000000000, target=0x2000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x2000, target=0x20, capture=False, promotion=10, castle=None, piece=1),
            Move(origin=0x1000000, target=0x4000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x2000, target=0x10, capture=True, promotion=11, castle=None, piece=1),
            Move(origin=0x800000000000, target=0x400000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000, target=0x20, capture=False, promotion=11, castle=None, piece=1),
            Move(origin=0x1000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x40000000000, target=0x20000000000, capture=True, promotion=None, castle=None, piece=7),
            Move(origin=0x1000000, target=0x1000000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x40000000000, target=0x800000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x1000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x1000000, target=0x20000, capture=True, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000, target=0x800000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x20000000000000, target=0x2000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x2000, target=0x10, capture=True, promotion=8, castle=None, piece=1),
            Move(origin=0x1000000, target=0x100000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x2000, target=0x10, capture=True, promotion=9, castle=None, piece=1),
            Move(origin=0x20000000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x40000000000, target=0x8000000000000, capture=True, promotion=None, castle=None, piece=7),
            Move(origin=0x2000, target=0x10, capture=True, promotion=10, castle=None, piece=1),
            Move(origin=0x1000000, target=0x10000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x40000000000, target=0x200000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x40000000000, target=0x4000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x800000000000, target=0x80000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x800000000000, target=0x8000000000, capture=False, promotion=None, castle=None, piece=5)
        }

        moves = set(all_moves(board))

        self.assertSetEqual(moves, expected_moves)


    def test_fen_2(self):
        # fen = "8/B7/1b1p1K2/Pr2P1P1/1P5R/3q3p/3r2p1/4k1N1 b - - 0 1"

        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [18155145947250688, 4611686018427387904, 131328, 2252349603053568, 8796093022208,
                        1152921504608944128, 1173337236545601536, 4611686578134188288]

        expected_moves = {
            Move(origin=0x80000000000, target=0x400000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x2000000, target=0x10000000, capture=True, promotion=None, castle=None, piece=5),
            Move(origin=0x20000, target=0x8, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=0x20000, target=0x4000000, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=0x80000000000, target=0x800000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000000, target=0x1000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000000, target=0x400000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x2000000, target=0x200000000, capture=True, promotion=None, castle=None, piece=5),
            Move(origin=0x800000000000, target=0x80000000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x8000000000000, target=0x4000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x80000000000, target=0x40000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000000, target=0x20000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x20000, target=0x1000000, capture=True, promotion=None, castle=None, piece=3),
            Move(origin=0x20000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=0x80000000000, target=0x10000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000, target=0x8000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x80000000000, target=0x400000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x1000000000000000, target=0x800000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x1000000000000000, target=0x2000000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x80000000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x2000000, target=0x1000000, capture=True, promotion=None, castle=None, piece=5),
            Move(origin=0x20000, target=0x400, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=0x8000000000000, target=0x800000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x20000, target=0x100, capture=True, promotion=None, castle=None, piece=3),
            Move(origin=0x80000000000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x1000000000000000, target=0x10000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x8000000000000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x20000, target=0x800000000, capture=False, promotion=None, castle=None, piece=3),
            Move(origin=0x80000000000, target=0x4000000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x20000, target=0x4000000000000000, capture=True, promotion=None, castle=None, piece=3),
            Move(origin=0x80000000000, target=0x10000000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x8000000000000, target=0x2000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x80000000000, target=0x20000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000000, target=0x2000000000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000000000, target=0x8000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x8000000000000, target=0x1000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000000, target=0x4000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x8000000000000, target=0x10000000000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x1000000000000000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x80000000000, target=0x200000000000000, capture=False, promotion=None, castle=None, piece=6),
            Move(origin=0x80000, target=0x10000000, capture=True, promotion=None, castle=None, piece=1),
            Move(origin=0x20000, target=0x100000000000, capture=False, promotion=None, castle=None, piece=3)
        }

        moves = set(all_moves(board))

        self.assertSetEqual(moves, expected_moves)


    def test_fen_3(self):
        # fen = "8/B7/3p1K2/Pr2p3/1P3p2/7p/6p1/4k1N1 b - - 0 1"

        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [18155282312462336, 4611686018427387904, 256, 33554432, 0, 1152921504608944128,
                        1171076778346151936, 4611686027036197120]

        expected_moves = {
            Move(origin=0x2000000, target=0x8000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000000, target=0x200, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x1000000000000000, target=0x800000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x1000000000000000, target=0x2000000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x2000000, target=0x20000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000000, target=0x1000000, capture=True, promotion=None, castle=None, piece=5),
            Move(origin=0x2000000000, target=0x200000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x2000000, target=0x2, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x2000000, target=0x4000000, capture=False, promotion=None, castle=None, piece=5),
            Move(origin=0x1000000000000000, target=0x8000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x1000000000000000, target=0x10000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x2000000, target=0x200000000, capture=True, promotion=None, castle=None, piece=5),
            Move(origin=0x1000000000000000, target=0x20000000000000, capture=False, promotion=None, castle=None, piece=7),
            Move(origin=0x80000, target=0x8000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x10000000, target=0x1000000000, capture=False, promotion=None, castle=None, piece=1),
            Move(origin=0x800000000000, target=0x80000000000000, capture=False, promotion=None, castle=None, piece=1)
        }

        moves = set(all_moves(board))

        self.assertSetEqual(moves, expected_moves)
