import copy

from core.utils import Board
from core.zuggenerator import generate, lsb_generator, check_for_check, check_king_hill, check_for_checkmate, hill, \
    check_for_remi, sort_weak_strong

pawnEvalBlack_list = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
a_1 = 0x8000000000000000
pawnEvalBlack = {}
for val in pawnEvalBlack_list:
    pawnEvalBlack[a_1] = val
    a_1 >>= 1

pawnEvalWhite_list = list(reversed(pawnEvalBlack_list))
a_1 = 0x8000000000000000
pawnEvalWhite = {}
for val in pawnEvalWhite_list:
    pawnEvalWhite[a_1] = val
    a_1 >>= 1

knightEval_list = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]
a_1 = 0x8000000000000000
knightEval = {}
for val in knightEval_list:
    knightEval[a_1] = val
    a_1 >>= 1

bishopEvalBlack_list = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
a_1 = 0x8000000000000000
bishopEvalBlack = {}
for val in bishopEvalBlack_list:
    bishopEvalBlack[a_1] = val
    a_1 >>= 1

bishopEvalWhite_list = list(reversed(bishopEvalBlack_list))
a_1 = 0x8000000000000000
bishopEvalWhite = {}
for val in bishopEvalWhite_list:
    bishopEvalWhite[a_1] = val
    a_1 >>= 1

rookEvalBlack_list = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
a_1 = 0x8000000000000000
rookEvalBlack = {}
for val in rookEvalBlack_list:
    rookEvalBlack[a_1] = val
    a_1 >>= 1

rookEvalWhite_list = list(reversed(rookEvalBlack_list))
a_1 = 0x8000000000000000
rookEvalWhite = {}
for val in rookEvalWhite_list:
    rookEvalWhite[a_1] = val
    a_1 >>= 1

queenEval_list = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]
a_1 = 0x8000000000000000
queenEval = {}
for val in queenEval_list:
    queenEval[a_1] = val
    a_1 >>= 1

kingEvalBlack_list = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, 0, 0, 0, 0, -20, -10,
    20, -30, -30, 100, 100, -30, -30, -20,
    -30, -40, -40, 100, 100, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
a_1 = 0x8000000000000000
kingEvalBlack = {}
for val in kingEvalBlack_list:
    kingEvalBlack[a_1] = val
    a_1 >>= 1

kingEvalWhite_list = list(reversed(kingEvalBlack_list))
a_1 = 0x8000000000000000
kingEvalWhite = {}
for val in kingEvalWhite_list:
    kingEvalWhite[a_1] = val
    a_1 >>= 1

kingEvalEndGameBlack_list = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
a_1 = 0x8000000000000000
kingEvalEndGameBlack = {}
for val in kingEvalEndGameBlack_list:
    kingEvalEndGameBlack[a_1] = val
    a_1 >>= 1

kingEvalEndGameWhite_list = list(reversed(kingEvalEndGameBlack_list))
a_1 = 0x8000000000000000
kingEvalEndGameWhite = {}
for val in kingEvalEndGameWhite_list:
    kingEvalEndGameWhite[a_1] = val
    a_1 >>= 1


def pst(board: Board):
    """
    Piece square Tables. Evaluates a board.
    Used by evaluate_board
    :param board: The board to be evaluated
    :return: total score according to piece-square-tables
    """
    piece_white = {
        'P': (board.pawns & board.white_pieces, pawnEvalWhite),
        'R': (board.rooks & board.white_pieces, rookEvalWhite),
        'N': (board.knights & board.white_pieces, knightEval),
        'B': (board.bishops & board.white_pieces, bishopEvalWhite),
        'Q': (board.queens & board.white_pieces, queenEval),
        'K': (board.kings & board.white_pieces, kingEvalWhite),
    }

    piece_black = {
        'p': (board.pawns & board.black_pieces, pawnEvalBlack),
        'r': (board.rooks & board.black_pieces, rookEvalBlack),
        'n': (board.knights & board.black_pieces, knightEval),
        'b': (board.bishops & board.black_pieces, bishopEvalBlack),
        'q': (board.queens & board.black_pieces, queenEval),
        'k': (board.kings & board.black_pieces, kingEvalBlack)
    }
    pst_score = 0
    for piece, (pieces, table) in piece_white.items():
        pst_score += evaluate_pst(pieces, table)
    for piece, (pieces, table) in piece_black.items():
        pst_score -= evaluate_pst(pieces, table)

    return pst_score


def evaluate_pst(piece_bb, table):
    """
    Helper funciton of pst.
    add tables for piece piece_bb
    :param piece_bb: The piece as int (bitboard)
    :param table: pst of the piece
    :return: score as int
    """
    score = 0
    # for square in range(64):
    #    if piece_bb & (1 << square):
    #        piece_value = table[square]  # Retrieve piece-square value
    #        score += piece_value  # Add piece-square value to score
    for bit in lsb_generator(piece_bb):
        score += table.get(bit)
    return score


def piece_mobile(board):
    """
    evaluate piece mobility.
    Used by evaluate_board.
    :param board: The board to be evaluated
    :return: evaluation as int
    """
    score = 0

    temp_board = copy.deepcopy(board)
    temp_board.active_color = not board.active_color

    if board.active_color:
        score += len(generate(board))
        score -= len(generate(temp_board))
    else:
        score -= len(generate(board))
        score += len(generate(temp_board))

    return score


def center_control(board):
    if board.active_color:
        return 30 * count_ones(board.white_pieces & hill)
    else:
        return 0


def evaluate_board(board: Board, sym: bool = False):
    """
    Evaluates a given Board.
    Used by alpha-beta, minimax and pvs.
    :param board: The Board to be evaluated
    :param sym: if set to True, the result will be symetric
    :return: Evaluation of Board as int
    """
    piece_values = {
        'P': (board.pawns & board.white_pieces, 100),
        'R': (board.rooks & board.white_pieces, 500),
        'N': (board.knights & board.white_pieces, 300),
        'B': (board.bishops & board.white_pieces, 300),
        'Q': (board.queens & board.white_pieces, 900),
        'p': (board.pawns & board.black_pieces, -100),
        'r': (board.rooks & board.black_pieces, -500),
        'n': (board.knights & board.black_pieces, -300),
        'b': (board.bishops & board.black_pieces, -300),
        'q': (board.queens & board.black_pieces, -900)
    }

    total_score = 0

    if check_for_checkmate(board):
        if not board.active_color:
            if sym:
                return float("-inf")
            else:
                return float("inf")
        else:
            return float("-inf")

    if check_king_hill(board):
        if not board.active_color:
            if sym:
                return float("-inf")
            else:
                return float("inf")
        else:
            return float("-inf")

    for piece, (pieces, value) in piece_values.items():
        total_score += count_ones(pieces) * value

    total_score += pst(board)

    # total_score += center_control(board)
    #
    # total_score += piece_mobile(board)
    #
    # if check_for_remi(board):
    #     total_score = -total_score

    if sym and not board.active_color:
        return -total_score

    return total_score


def count_ones(binary_number):
    """
    Count bits set to one in binary number
    :param binary_number: number as int
    :return: the number of ones
    """
    return bin(binary_number).count("1")


def quiescient_search(board, alpha, beta, depth):
    """
    Perform a Quiescence Search on the given board to evaluate it.
    Used by pvs_sorted_multi_qs and pvs_sorted_qs
    :param board: The current Board
    :param alpha: The alpha value
    :param beta: The beta value
    :param depth: The maximum depth. Smaller means faster
    :return: evaluation of board as int
    """

    stand_pat = evaluate_board(board, sym=True)
    if depth == 3:
        return stand_pat
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    temp_board = copy.deepcopy(board)
    my_moves = generate(board)
    my_moves = sort_weak_strong(my_moves)

    for mmove in my_moves:
        temp_board.do_move(mmove)
        score = -quiescient_search(board, -beta, -alpha, depth+1)
        opp_moves = generate(temp_board)
        opp_moves = sort_weak_strong(opp_moves)
        if not opp_moves:
            break
        omove = opp_moves.pop(0)
        temp_board.do_move(omove)
        if score >= beta:
            return beta

        if score > alpha:
            alpha = score

    return alpha
