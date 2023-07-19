from context import Board, Move, get_lsb, pop_lsb, get_first_set_bit_position
from context import fen_split, fen_to_bitboards, get_empty_squares_bitboard
from context import print_bitboards, print_bitboard
from context import gen_all_masks

import unittest
import copy


class BoardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        gen_all_masks()

    @classmethod
    def tearDown(self) -> None:
        pass

    def test_boolean_attributes(self):
        board = Board()
        board.active_color = True
        board.castling_bk = True
        board.castling_wk = True
        board.castling_bq = True
        board.castling_wq = True

        self.assertEquals(board.active_color, True)
        self.assertEquals(board.castling_bk, True)
        self.assertEquals(board.castling_wk, True)
        self.assertEquals(board.castling_bq, True)
        self.assertEquals(board.castling_wq, True)

        board.active_color = False
        board.castling_bk = False
        board.castling_wk = False
        board.castling_bq = False
        board.castling_wq = False

        self.assertEquals(board.active_color, False)
        self.assertEquals(board.castling_bk, False)
        self.assertEquals(board.castling_wk, False)
        self.assertEquals(board.castling_bq, False)
        self.assertEquals(board.castling_wq, False)

    def test_boards_get_set(self):
        boards = [
            0x1,
            0x2,
            0x3,
            0x4,
            0x5,
            0x6,
            0x7,
            0x8,
        ]
        board = Board()
        board.boards = boards
        self.assertEquals(board.pawns, boards[0])
        self.assertEquals(board.knights, boards[1])
        self.assertEquals(board.bishops, boards[2])
        self.assertEquals(board.rooks, boards[3])
        self.assertEquals(board.queens, boards[4])
        self.assertEquals(board.kings, boards[5])
        self.assertEquals(board.black_pieces, boards[6])
        self.assertEquals(board.white_pieces, boards[7])


    def test_deepcopy(self):
        # since we implemented our own __deepopy__ method
        boards = [
            0x1,
            0x2,
            0x3,
            0x4,
            0x5,
            0x6,
            0x7,
            0x8,
        ]
        board = Board()
        board.boards = boards
        board.active_color = True
        board.castling_bk = True
        board.castling_wk = True
        board.castling_bq = True
        board.castling_wq = True

        copy_board = board.__deepcopy__()

        # check if copy_board is a new object, not a reference
        self.assertIsNot(copy_board, board)

        self.assertEquals(copy_board.boards, board.boards)

        self.assertEquals(copy_board.active_color, board.active_color)
        self.assertEquals(copy_board.castling_bk, board.castling_bk)
        self.assertEquals(copy_board.castling_wk, board.castling_wk)
        self.assertEquals(copy_board.castling_bq, board.castling_bq)
        self.assertEquals(copy_board.castling_wq, board.castling_wq)


    def test_iter(self):
        # since the board class is iterable
        boards = [
            0x1,
            0x2,
            0x3,
            0x4,
            0x5,
            0x6,
            0x7,
            0x8,
        ]
        board = Board()
        board.boards = boards
        board.active_color = True
        board.castling_bk = True
        board.castling_wk = True
        board.castling_bq = True
        board.castling_wq = True

        generator_as_list = list(board.__iter__())

        self.assertEquals(generator_as_list, boards)


    def test_do_move(self):
        # fen = 8/B7/3p1K2/Pr2p3/1P3p2/7p/6p1/4k1N1 b - - 0 1
        gen_all_masks()
        board = Board()

        board.active_color = False
        board.castling_bk = False
        board.castling_bq = False
        board.castling_wk = False
        board.castling_wq = False
        board.boards = [18155282312462336, 4611686018427387904, 256, 33554432, 0, 1152921504608944128,
                        1171076778346151936, 4611686027036197120]

        moved_board = Board()

        moved_board.active_color = True
        moved_board.castling_bk = False
        moved_board.castling_bq = False
        moved_board.castling_wk = False
        moved_board.castling_wq = False
        moved_board.boards = [18155282312462336, 4611686018427387904, 256, 2, 0, 1152921504608944128,
                              1171076778312597506, 4611686027036197120]

        move = Move(origin=33554432, target=2, capture=False, promotion=None, castle=None)

        board.do_move(move)

        self.assertIsNot(moved_board, board)

        self.assertEquals(moved_board.boards, board.boards)

        self.assertEquals(moved_board.active_color, board.active_color)
        self.assertEquals(moved_board.castling_bk, board.castling_bk)
        self.assertEquals(moved_board.castling_wk, board.castling_wk)
        self.assertEquals(moved_board.castling_bq, board.castling_bq)
        self.assertEquals(moved_board.castling_wq, board.castling_wq)


class MoveTests(unittest.TestCase):

    def test_constructor_no_input(self):
        move = Move()

        self.assertEquals(move.origin, None)
        self.assertEquals(move.target, None)
        self.assertEquals(move.capture, None)
        self.assertEquals(move.promotion, None)
        self.assertEquals(move.castle, None)

    def test_constructor_with_input_no_castle(self):
        move = Move(origin=0x1, target=0x2, capture=False, promotion=False)

        self.assertEquals(move.origin, 0x1)
        self.assertEquals(move.target, 0x2)
        self.assertEquals(move.capture, False)
        self.assertEquals(move.promotion, False)
        self.assertEquals(move.castle, None)

    def test_constructor_with_castle(self):
        rook_move = Move(origin=1, target=4, capture=False, promotion=False)
        king_move = Move(origin=8, target=2, capture=False, promotion=False, castle=rook_move)

        self.assertEquals(rook_move.origin, 1)
        self.assertEquals(rook_move.target, 4)
        self.assertEquals(rook_move.capture, False)
        self.assertEquals(rook_move.promotion, False)
        self.assertEquals(rook_move.castle, None)

        self.assertEquals(king_move.origin, 8)
        self.assertEquals(king_move.target, 2)
        self.assertEquals(king_move.capture, False)
        self.assertEquals(king_move.promotion, False)
        self.assertEquals(king_move.castle, rook_move)

    def test_eq(self):
        move_1 = Move(origin=0x1, target=0x2, capture=False, promotion=False)
        move_2 = Move(origin=0x1, target=0x2, capture=False, promotion=False)

        self.assertTrue(move_1.__eq__(move_2))

        move_3 = Move(origin=0x1, target=0x2, capture=False, promotion=True)

        self.assertFalse(move_1.__eq__(move_3))


class BitCountOperationsTests(unittest.TestCase):
    pass



