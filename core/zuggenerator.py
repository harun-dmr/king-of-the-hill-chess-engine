import numpy as np
import random
from core.utils import fen_to_bitboards, fen_split, get_empty_squares_bitboard, Board, Move
import copy

# Define the bitboard constants for the chess board

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

hill = 0x1818000000

center = 0x0000001818000000
king_side = 0x000000000000007F
queen_side = 0x7F00000000000000

# Define the move offsets for each piece type
knight_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
bishop_offsets = [-9, -7, 7, 9]
rook_offsets = [-8, -1, 1, 8]
queen_offsets = bishop_offsets + rook_offsets

KNIGHT_MASKS = {0: 0}
ROOK_MASKS_N = {0: 0}
ROOK_MASKS_S = {0: 0}
ROOK_MASKS_E = {0: 0}
ROOK_MASKS_W = {0: 0}
BISHOP_MASKS_NE = {0: 0}
BISHOP_MASKS_NW = {0: 0}
BISHOP_MASKS_SE = {0: 0}
BISHOP_MASKS_SW = {0: 0}
KING_MASKS = {0: 0}


# QUEEN_MASKS = {}


def index_to_board(index: tuple):
    """
    Generate a bitboard with one bit set to one at index, where index is the index of the position in an 8 x 8 Matrix
    """
    start_pos = 0x8000000000000000

    return start_pos >> (index[0] * 8 + index[1])


def gen_kngiht_masks():
    """
    Generate Knight mask for every square and store it in KNIGHT_MASKS
    """

    for i in range(8):
        for j in range(8):
            index = (i, j)

            moves = []

            # possible moves for the knight
            moveset = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

            # iterate over each possible move
            for move in moveset:
                # calculate the new position
                new_pos = (index[0] + move[0], index[1] + move[1])
                # check if the new position is on the board
                if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    moves.append(index_to_board(new_pos))

            mask = 0x0

            for move in moves:
                mask |= move

            KNIGHT_MASKS[index_to_board(index)] = mask
            moves = []


def gen_rook_masks():
    """
    Generate all rook masks for every square and store them in ROOK_MASKS
    """
    for i in range(8):
        for j in range(8):
            index = (i, j)

            moves = [[], [], [], []]

            # possible moves for the knight
            moveset = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            # iterate over each possible move
            for z, move in enumerate(moveset):
                # calculate the new position
                new_pos = (index[0] + move[0], index[1] + move[1])
                # keep moving in the same move until the edge of the board or a piece is reached
                while 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    moves[z].append(index_to_board(new_pos))
                    new_pos = (new_pos[0] + move[0], new_pos[1] + move[1])

            mask = 0x0
            for move in moves[0]:
                mask |= move
            ROOK_MASKS_S[index_to_board(index)] = mask

            mask = 0x0
            for move in moves[1]:
                mask |= move
            ROOK_MASKS_N[index_to_board(index)] = mask

            mask = 0x0
            for move in moves[2]:
                mask |= move
            ROOK_MASKS_E[index_to_board(index)] = mask

            mask = 0x0
            for move in moves[3]:
                mask |= move
            ROOK_MASKS_W[index_to_board(index)] = mask


def gen_bishop_masks():
    """
    Generate all bishop masks and store them in BISHOP_MASKS
    """
    for i in range(8):
        for j in range(8):
            index = (i, j)

            moves = [[], [], [], []]

            # possible moves for the knight
            moveset = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

            # iterate over each possible move
            for z, move in enumerate(moveset):
                # calculate the new position
                new_pos = (index[0] + move[0], index[1] + move[1])
                # keep moving in the same move until the edge of the board or a piece is reached
                while 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    moves[z].append(index_to_board(new_pos))
                    new_pos = (new_pos[0] + move[0], new_pos[1] + move[1])

            mask = 0x0
            for move in moves[0]:
                mask |= move
            BISHOP_MASKS_SE[index_to_board(index)] = mask

            mask = 0x0
            for move in moves[1]:
                mask |= move
            BISHOP_MASKS_SW[index_to_board(index)] = mask

            mask = 0x0
            for move in moves[2]:
                mask |= move
            BISHOP_MASKS_NE[index_to_board(index)] = mask

            mask = 0x0
            for move in moves[3]:
                mask |= move
            BISHOP_MASKS_NW[index_to_board(index)] = mask

            moves = []


def gen_king_masks():
    """
    Generate all king masks and store them in KING_MASKS
    """
    for i in range(8):
        for j in range(8):
            index = (i, j)

            moves = []

            # possible moves for the knight
            moveset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            # iterate over each possible move
            for move in moveset:
                # calculate the new position
                new_pos = (index[0] + move[0], index[1] + move[1])
                # check if the new position is on the board
                if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    moves.append(index_to_board(new_pos))

            mask = 0x0

            for move in moves:
                mask |= move

            KING_MASKS[index_to_board(index)] = mask
            moves = []


def gen_queen_masks():
    # for key, value in ROOK_MASKS.items():
    #    QUEEN_MASKS[key] = value | BISHOP_MASKS.get(key)
    pass


def gen_all_masks():
    gen_kngiht_masks()
    gen_rook_masks()
    gen_bishop_masks()
    gen_king_masks()
    # gen_queen_masks() # must be generated after bishop and rook


def get_lsb(number):
    """
    Get last set bit (bit set to 1) of intger number
    """
    return number & (~number + 1)


def pop_lsb(number):
    """
    Pop the last set bi t of integer number
    """
    lsb = get_lsb(number)
    number ^= lsb
    return number, lsb


def lsb_generator(number):
    """
    generator of all set bits of number (can iterate over it)
    """
    while number:
        number, lsb = pop_lsb(number)
        yield lsb


def pawn_moves(board: Board):
    moves = []

    active_color = board.active_color

    if active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    empty_squares = ~(active_pieces | passive_pieces) & 0xFFFFFFFFFFFFFFFF

    pawns = board.pawns & active_pieces

    # bitboards for move straight or hit diagonally
    if active_color:
        move_straight = ((pawns & ~rank_8) >> 8) & empty_squares
        move_straight_og = (move_straight << 8) & pawns

        move_double = ((((pawns & rank_2) >> 8) & empty_squares) >> 8) & empty_squares
        move_double_og = (move_straight << 16) & pawns

        attack_right = ((pawns & ~h_file) >> 7) & passive_pieces
        attack_right_og = (move_straight << 7) & pawns

        attack_left = ((pawns & ~a_file) >> 9) & passive_pieces
        attack_left_og = (move_straight << 9) & pawns

    else:
        move_straight = ((pawns & ~rank_1) << 8) & empty_squares
        move_straight_og = (move_straight >> 8) & pawns

        move_double = ((((pawns & rank_7) << 8) & empty_squares) << 8) & empty_squares
        move_double_og = (move_straight >> 16) & pawns

        attack_right = ((pawns & ~a_file) << 7) & passive_pieces
        attack_right_og = (move_straight >> 7) & pawns

        attack_left = ((pawns & ~h_file) << 9) & passive_pieces
        attack_left_og = (move_straight >> 9) & pawns

    for target in lsb_generator(move_straight):
        if active_color:
            pos = target << 8
        else:
            pos = target >> 8
        capture = target & passive_pieces != 0

        res = Move(pos, target, capture, piece=1)

        if target & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    for target in lsb_generator(move_double):
        if active_color:
            pos = target << 16
        else:
            pos = target >> 16
        capture = target & passive_pieces != 0

        res = Move(pos, target, capture, piece=1)

        if target & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    for target in lsb_generator(attack_right):
        if active_color:
            pos = target << 7
        else:
            pos = target >> 7
        capture = target & passive_pieces != 0

        res = Move(pos, target, capture, piece=1)

        if target & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    for target in lsb_generator(attack_left):
        if active_color:
            pos = target << 9
        else:
            pos = target >> 9
        capture = target & passive_pieces != 0

        res = Move(pos, target, capture, piece=1)

        if target & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    return moves


def pawn_moves_pos(board: Board, pos: int = None):
    moves = []

    active_color = board.active_color

    if active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    empty_squares = ~(active_pieces | passive_pieces) & 0xFFFFFFFFFFFFFFFF

    pawns = pos

    # bitboards for move straight or hit diagonally
    if active_color:
        move_straight = ((pawns & ~rank_8) >> 8) & empty_squares

        move_double = ((((pawns & rank_2) >> 8) & empty_squares) >> 8) & empty_squares

        attack_right = ((pawns & ~h_file) >> 7) & passive_pieces

        attack_left = ((pawns & ~a_file) >> 9) & passive_pieces

    else:
        move_straight = ((pawns & ~rank_1) << 8) & empty_squares

        move_double = ((((pawns & rank_7) << 8) & empty_squares) << 8) & empty_squares

        attack_right = ((pawns & ~a_file) << 7) & passive_pieces

        attack_left = ((pawns & ~h_file) << 9) & passive_pieces

    if move_straight:
        res = Move(pos, move_straight, False, piece=1)
        if move_straight & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    if move_double:
        res = Move(pos, move_double, False, piece=1)
        moves.append(res)

    if attack_right:
        res = Move(pos, attack_right, True, piece=1)
        if attack_right & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    if attack_left:
        res = Move(pos, attack_left, True, piece=1)
        if attack_left & (rank_1 | rank_8):
            if active_color:
                qm = copy.deepcopy(res)
                qm.promotion = 8
                rm = copy.deepcopy(res)
                rm.promotion = 9
                nm = copy.deepcopy(res)
                nm.promotion = 10
                bm = copy.deepcopy(res)
                bm.promotion = 11
            else:
                qm = copy.deepcopy(res)
                qm.promotion = 2
                rm = copy.deepcopy(res)
                rm.promotion = 3
                nm = copy.deepcopy(res)
                nm.promotion = 4
                bm = copy.deepcopy(res)
                bm.promotion = 5
            moves.extend([qm, rm, nm, bm])
        else:
            moves.append(res)

    return moves


def knight_moves(board: Board, pos: int = None):
    """
    Return all possible kngiht moves of board.active_color.
    If pos is set to a bitboard with exactly one pieces location,
    knight moves will be generated from this location.
    """
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    if pos is not None:
        for target in lsb_generator(KNIGHT_MASKS.get(pos) & ~active_pieces):
            capture = target & passive_pieces != 0
            moves.append(Move(pos, target, capture, piece=2))
    else:
        knights = board.knights & active_pieces

        for knight in lsb_generator(knights):
            for target in lsb_generator(KNIGHT_MASKS.get(knight) & ~active_pieces):
                capture = target & passive_pieces != 0
                moves.append(Move(knight, target, capture, piece=2))

    return moves


def rook_moves(board, pos):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    # east
    temp_pos = pos
    h_file = 0x0101010101010101
    while temp_pos & ~h_file:
        temp_pos >>= 1
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=5))
        if capture: break

    # west
    temp_pos = pos
    a_file = 0x8080808080808080
    while temp_pos & ~a_file:
        temp_pos <<= 1
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=5))
        if capture: break

    # north
    temp_pos = pos
    rank_8 = 0xFF00000000000000
    while temp_pos & ~rank_8:
        temp_pos <<= 8
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=5))
        if capture: break

    # south
    temp_pos = pos
    rank_1 = 0xFF
    while temp_pos & ~rank_1:
        temp_pos >>= 8
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=5))
        if capture: break

    return moves


def rook_moves_not_working(board: Board, pos: int):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    n_mask = ROOK_MASKS_N.get(pos)
    blocking_pieces = n_mask & active_pieces
    blocker = pop_lsb(blocking_pieces)[1]
    blocker_path = ROOK_MASKS_S.get(blocker)
    final_path = n_mask
    if blocker_path:
        final_path = n_mask & blocker_path

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (ROOK_MASKS_S.get(blocker) << 8) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    mask = ROOK_MASKS_S.get(pos)
    blocker = pop_lsb(mask & active_pieces)[1]
    final_path = mask & ROOK_MASKS_N.get(blocker) if blocker != 0 else mask

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (ROOK_MASKS_N.get(blocker) >> 8) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    mask = ROOK_MASKS_W.get(pos)
    blocker = pop_lsb(mask & active_pieces)[1]
    final_path = mask & ROOK_MASKS_E.get(blocker) if blocker != 0 else mask

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (ROOK_MASKS_E.get(blocker) << 1) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    mask = ROOK_MASKS_E.get(pos)
    blocker = pop_lsb(mask & active_pieces)[1]
    final_path = mask & ROOK_MASKS_W.get(blocker) if blocker != 0 else mask

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (ROOK_MASKS_W.get(blocker) >> 1) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    return moves


def rooks_moves(board: Board):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    rooks = board.rooks & active_pieces
    for rook in lsb_generator(rooks):
        moves.extend(rook_moves(board, rook))

    return moves


def bishop_moves(board: Board, pos: int):
    moves = []

    h_file = 0x0101010101010101
    rank_1 = 0xFF
    a_file = 0x8080808080808080
    rank_8 = 0xFF00000000000000

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    # se
    temp_pos = pos
    while temp_pos & ~(h_file | rank_1):
        temp_pos >>= 9
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=3))
        if capture: break

    # nw
    temp_pos = pos
    while temp_pos & ~(a_file | rank_8):
        temp_pos <<= 9
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=3))
        if capture: break

    # ne
    temp_pos = pos
    while temp_pos & ~(rank_8 | h_file):
        temp_pos <<= 7
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=3))
        if capture: break

    # sw
    temp_pos = pos
    while temp_pos & ~(rank_1 | a_file):
        temp_pos >>= 7
        if temp_pos & active_pieces: break
        capture = temp_pos & passive_pieces != 0
        moves.append(Move(pos, temp_pos, capture, piece=3))
        if capture: break

    return moves


def bishop_moves_not_working(board: Board, pos: int):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    n_mask = BISHOP_MASKS_NW.get(pos)
    blocking_pieces = n_mask & active_pieces
    blocker = pop_lsb(blocking_pieces)[1]
    blocker_path = BISHOP_MASKS_SE.get(blocker)

    final_path = n_mask
    if blocker_path:
        final_path = n_mask & blocker_path

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (BISHOP_MASKS_SE.get(blocker) << 9) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    mask = BISHOP_MASKS_NE.get(pos)
    blocker = pop_lsb(mask & active_pieces)[1]
    final_path = mask & BISHOP_MASKS_SW.get(blocker) if blocker != 0 else mask

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (BISHOP_MASKS_SW.get(blocker) << 7) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    mask = BISHOP_MASKS_SW.get(pos)
    blocker = pop_lsb(mask & active_pieces)[1]
    final_path = mask & BISHOP_MASKS_NE.get(blocker) if blocker != 0 else mask

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (BISHOP_MASKS_NE.get(blocker) >> 7) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    mask = BISHOP_MASKS_SE.get(pos)
    blocker = pop_lsb(mask & active_pieces)[1]
    final_path = mask & BISHOP_MASKS_NW.get(blocker) if blocker != 0 else mask

    blocker = pop_lsb(final_path & passive_pieces)[1]
    final_path = final_path & (BISHOP_MASKS_NW.get(blocker) >> 9) if blocker != 0 else final_path

    for target in lsb_generator(final_path):
        moves.append(Move(pos, target, target & passive_pieces != 0))

    # for target in lsb_generator(final_path):
    #    capture = target & passive_pieces != 0
    #    moves.append(Move(pos, target, capture))
    #    if capture: break

    return moves


def bishops_moves(board: Board):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    bishops = board.bishops & active_pieces
    for bishop in lsb_generator(bishops):
        moves.extend(bishop_moves(board, bishop))

    return moves


def queen_moves(board: Board, pos: int = None):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    if pos is None:
        pos = board.queens & active_pieces

    moves.extend(bishop_moves(board, pos))
    moves.extend(rook_moves(board, pos))

    for move in moves:
        setattr(move, "piece", 6)

    return moves


def king_moves(board: Board, pos: int = None, check: bool = True):
    moves = []

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    if pos is None:
        pos = board.kings & active_pieces

    for target in lsb_generator(KING_MASKS.get(pos) & ~active_pieces):
        capture = target & passive_pieces != 0
        moves.append(Move(pos, target, capture, piece=7))

    # castling
    if check:
        tmp_board = copy.deepcopy(board)
        if not board.active_color and board.castling_bk:
            if not ((0xE & (active_pieces | passive_pieces)) or check_for_check(tmp_board, pos >> 4) or check_for_check(tmp_board, pos >> 3) or check_for_check(tmp_board, pos) or check_for_check(tmp_board, pos >> 2) or check_for_check(tmp_board, pos >> 1)):
                moves.append(Move(pos, pos >> 2, castle=Move(pos >> 4, pos >> 1), piece=7))

        if not board.active_color and board.castling_bq:
            if not ((0x60 & (active_pieces | passive_pieces)) or check_for_check(tmp_board, pos << 3) or check_for_check(tmp_board, pos << 2) or check_for_check(tmp_board, pos << 1) or check_for_check(tmp_board, pos)):
                moves.append(Move(pos, pos << 2, castle=Move(pos << 3, pos << 1), piece=7))

        if board.active_color and board.castling_wk:
            if not ((0xE00000000000000 & (active_pieces | passive_pieces)) or check_for_check(tmp_board, pos >> 4) or check_for_check(tmp_board, pos >> 3) or check_for_check(tmp_board, pos) or check_for_check(tmp_board, pos >> 2) or check_for_check(tmp_board, pos >> 1)):
                moves.append(Move(pos, pos >> 2, castle=Move(pos >> 4, pos >> 1), piece=7))

        if board.active_color and board.castling_wq:
            if not ((0x6000000000000000 & (active_pieces | passive_pieces)) or check_for_check(tmp_board, pos << 3) or check_for_check(tmp_board, pos << 2) or check_for_check(tmp_board, pos << 1) or check_for_check(tmp_board, pos)):
                moves.append(Move(pos, pos << 2, castle=Move(pos << 3, pos << 1), piece=7))

    return moves


def all_moves(board: Board):
    moves = pawn_moves(board) + rooks_moves(board) + knight_moves(board) + bishops_moves(board) + queen_moves(
        board) + king_moves(board)

    return moves


def check_for_check(board: Board, pos: int = None):
    checked = False

    if board.active_color:
        active_pieces = board.white_pieces
        passive_pieces = board.black_pieces
    else:
        active_pieces = board.black_pieces
        passive_pieces = board.white_pieces

    if pos is None:
        pos = board.kings & active_pieces

    # qm = queen_moves(board, pos)
    # qp = 0
    # for move in qm:
    #    qp |= move.target

    for move in queen_moves(board, pos):
        if move.capture and (move.target & (board.queens & passive_pieces)):
            return True
    for move in knight_moves(board, pos):
        if move.capture and move.target & board.knights & passive_pieces:
            return True
    for move in pawn_moves_pos(board, pos):
        if move.capture and move.target & board.pawns & passive_pieces:
            return True
    for move in king_moves(board, pos, False):
        if move.capture and move.target & board.kings & passive_pieces:
            return True
    for move in rook_moves(board, pos):
        if move.capture and move.target & board.rooks & passive_pieces:
            return True
    for move in bishop_moves(board, pos):
        if move.capture and move.target & board.bishops & passive_pieces:
            return True

    return False


def check_for_checkmate(board: Board, pos: int = None):
    checked = False

    if pos is None:
        if board.active_color:
            active_pieces = board.white_pieces
            passive_pieces = board.black_pieces
        else:
            active_pieces = board.black_pieces
            passive_pieces = board.white_pieces

        pos = board.kings & active_pieces

    if check_for_check(board, pos):
        if not generate(board):
            return True

    return False


def check_king_hill(board: Board, pos: int = None):
    if pos is None:
        if board.active_color:
            active_pieces = board.white_pieces
            passive_pieces = board.black_pieces
        else:
            active_pieces = board.black_pieces
            passive_pieces = board.white_pieces

        pos = board.kings & active_pieces

    if pos & hill:
        return True

    return False


def check_for_remi(board: Board):
    if not (generate(board) or check_for_check(board)):
        return True
    return False


def game_ending(board: Board):
    if check_king_hill(board):
        return True
    elif not generate(board):
        return True
    return False


def generate(board: Board):
    if board.moves is None:
        moves = all_moves(board)

        legal_moves = []
        for move in moves:
            temp_board = copy.deepcopy(board)
            temp_board.do_move(move)
            temp_board.active_color = not temp_board.active_color
            if not check_for_check(temp_board):
                legal_moves.append(move)
        board.moves = legal_moves
    return board.moves


def sort_moves(moves):
    # Sort the moves based on the 'capture' attribute.
    # Moves with 'capture=True' will come before moves with 'capture=False'.
    sorted_moves = sorted(moves, key=lambda move: not move.capture)
    return sorted_moves


def sort_weak_strong(moves):
    # Filter out the moves with 'capture=False'
    capture_moves = [move for move in moves if move.capture]
    # Sort the capture moves based on the 'piece' attribute.
    sorted_moves = sorted(capture_moves, key=lambda move: move.piece)
    return sorted_moves


def square_to_bit(file, rank):
    files = "abcdefgh"
    ranks = "87654321"

def random_pawn_move(board):
    if board.active_color:
        active_pieces = board.white_pieces
    else:
        active_pieces = board.black_pieces
    mask = board.pawns & active_pieces
    if not mask:
        return False
    locations = list(lsb_generator(mask))
    piece = random.choice(locations)
    moves = pawn_moves_pos(board, piece)
    if not moves:
        return False
    return random.choice(moves)

def random_knight_move(board):
    if board.active_color:
        active_pieces = board.white_pieces
    else:
        active_pieces = board.black_pieces
    mask = board.knights & active_pieces
    if not mask:
        return False
    locations = list(lsb_generator(mask))
    piece = random.choice(locations)
    moves = knight_moves(board, piece)
    if not moves:
        return False
    return random.choice(moves)

def random_bishop_move(board):
    if board.active_color:
        active_pieces = board.white_pieces
    else:
        active_pieces = board.black_pieces
    mask = board.bishops & active_pieces
    if not mask:
        return False
    locations = list(lsb_generator(mask))
    piece = random.choice(locations)
    moves = bishop_moves(board, piece)
    if not moves:
        return False
    return random.choice(moves)

def random_rook_move(board):
    if board.active_color:
        active_pieces = board.white_pieces
    else:
        active_pieces = board.black_pieces
    mask = board.rooks & active_pieces
    if not mask:
        return False
    locations = list(lsb_generator(mask))
    piece = random.choice(locations)
    moves = rook_moves(board, piece)
    if not moves:
        return False
    return random.choice(moves)

def random_queen_move(board):
    if board.active_color:
        active_pieces = board.white_pieces
    else:
        active_pieces = board.black_pieces
    mask = board.queens & active_pieces
    if not mask:
        return False
    moves = queen_moves(board, mask)
    if not moves:
        return False
    return random.choice(moves)

def random_king_move(board):
    if board.active_color:
        active_pieces = board.white_pieces
    else:
        active_pieces = board.black_pieces
    mask = board.kings & active_pieces
    if not mask:
        return False
    moves = king_moves(board, mask)
    if not moves:
        return False
    return random.choice(moves)


def random_legal_move(board, iterations=10):
    if iterations == 0:
        return False, False
    l = [
        random_pawn_move, random_knight_move, random_bishop_move,
        random_rook_move, random_queen_move, random_king_move
    ]

    random_num = random.randint(0,5)
    move = l[random_num](board)
    if move == False:
        return random_legal_move(board, iterations - 1)
    test_board = copy.deepcopy(board)
    #test_board = board.__deepcopy__()
    test_board.do_move(move)
    test_board.active_color = not test_board.active_color
    if check_for_checkmate(test_board):
        return random_legal_move(board, iterations - 1)
    else:
        test_board.active_color = not test_board.active_color
    return move, test_board






# def square_to_bit(file, rank):
#     files = "abcdefgh"
#     ranks = "87654321"
#
#     if file not in files or rank not in ranks:
#         return None
#
#     file_index = files.index(file)
#     rank_index = ranks.index(rank)
#
#     bit_number = 1 << (file_index + 8 * rank_index)
#     return bit_number

    file_index = files.index(file)
    rank_index = ranks.index(rank)

    bit_number = 1 << (file_index + 8 * rank_index)
    return bit_number


if __name__ == "__main__":
    from utils import print_bitboard
    # print("h1")
    # print_bitboard(square_to_bit("h", "1"))
    # print("f1")
    # print_bitboard(square_to_bit("f", "1"))
    # print("e1")
    # print_bitboard(square_to_bit("e", "1"))
    # print("d1")
    # print_bitboard(square_to_bit("d", "1"))
    # print("b1")
    # print_bitboard(square_to_bit("b", "1"))
    # print("a1")
    # print_bitboard(square_to_bit("a", "1"))

    # print_bitboard(0x6000000000000000)
    # print_bitboard(6)

    # gen_all_masks()
    # board = Board("rnbQk2r/ppppp2p/6p1/8/8/8/PPPPPPPP/RNB1KBNR b KQkq - 0 1")
    #
    # pos = board.white_pieces & board.kings

    # print_bitboard(pos)
    # print("----------")
    # # print_bitboard(pos << 1)
    # print_bitboard(0xE)
    # print("----------")
    # # print_bitboard(pos << 1)
    # print_bitboard(0x60)
    # print("----------")
    # # print_bitboard(pos << 1)
    # print_bitboard(0xE00000000000000)
    # print("----------")
    # # print_bitboard(pos << 1)
    # print_bitboard(0x6000000000000000)
    # for move in generate(board):
    #     print(move)

    # gen_all_masks()
    # fen = "8/B7/3p1K2/Pr2p3/1P3p2/7p/6p1/4k1N1 b - - 0 1"
    # board = Board(fen)
    # print(f"# fen = \"{fen}\"")
    # print("")
    # print("board = Board()")
    # print("")
    # print(f"board.active_color = {board.active_color}")
    # print(f"board.castling_bk = {board.castling_bk}")
    # print(f"board.castling_bq = {board.castling_bq}")
    # print(f"board.castling_wk = {board.castling_wk}")
    # print(f"board.castling_wq = {board.castling_wq}")
    # board_boards = ', '.join([str(board.boards[i]) for i in range(8)])
    # print(f"board.boards = [{board_boards}]")
    # print("")
    # print("expected_moves = {")
    # for move in all_moves(board):
    #     print(f"Move(origin={move.origin}, target={move.target}, capture={move.capture}, promotion={move.promotion}, castle={move.castle}),")
    # print("}")
    # print("")
    # print("moves = set(all_moves(board))")
    # print("")
    # print("self.assertSetEqual(moves, expected_moves)")
    #



    # gen_all_masks()
    # fen = "8/B7/3p1K2/Pr2p3/1P3p2/7p/6p1/4k1N1 b - - 0 1"
    # board = Board(fen)
    # mboard = Board(fen)
    # moves = generate(board)
    # i = round(len(moves)/3) * 2
    # move = moves[i]
    # mboard.do_move(move)
    # print(f"# fen = {fen}")
    # print("")
    # print("board = Board()")
    # print("")
    # print(f"board.active_color = {board.active_color}")
    # print(f"board.castling_bk = {board.castling_bk}")
    # print(f"board.castling_bq = {board.castling_bq}")
    # print(f"board.castling_wk = {board.castling_wk}")
    # print(f"board.castling_wq = {board.castling_wq}")
    # board_boards = ', '.join([str(board.boards[i]) for i in range(8)])
    # print(f"board.boards = [{board_boards}]")
    # print("")
    # print("moved_board = Board()")
    # print("")
    # print(f"moved_board.active_color = {mboard.active_color}")
    # print(f"moved_board.castling_bk = {mboard.castling_bk}")
    # print(f"moved_board.castling_bq = {mboard.castling_bq}")
    # print(f"moved_board.castling_wk = {mboard.castling_wk}")
    # print(f"moved_board.castling_wq = {mboard.castling_wq}")
    # board_boards = ', '.join([str(mboard.boards[i]) for i in range(8)])
    # print(f"moved_board.boards = [{board_boards}]")
    # print("")
    # print(f"move = Move(origin={move.origin}, target={move.target}, capture={move.capture}, promotion={move.promotion}, castle={move.castle})")
    # print("")
    # print("board.do_move(move)")
    # print("")
    # print("self.assertEqual(board, moved_board)")




    # moved_board = Board()
    #
    # moved_board.active_color = True
    # moved_board.castling_bk = False
    # moved_board.castling_bq = False
    # moved_board.castling_wk = False
    # moved_board.castling_wq = False
    # moved_board.boards = [18155282312462336, 4611686018427387904, 256, 2, 0, 1152921504608944128, 1171076778312597506,
    #                       4611686027036197120]
    #
    # print(moved_board)