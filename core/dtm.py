from core.utils import Board



def dynamic_time_management(board: Board, time):
    """
    Calculate how much time should be appointed to generating the next move of boards active color.
    :param board: The current board
    :param time: players time left
    :return: the time that should be appointed as float
    """
    white_pieces_count = count_set_bits(board.white_pieces)
    black_pieces_count = count_set_bits(board.black_pieces)

    if white_pieces_count == black_pieces_count:
        return time / 20.0

    active_color = board.active_color

    if active_color:
        if white_pieces_count > black_pieces_count:
            if count_set_bits(board.queens & board.white_pieces) == 1 or \
                    count_set_bits(board.bishops & board.white_pieces) == 1 or \
                    count_set_bits(board.rooks & board.white_pieces) == 1:
                return time / 10.0
            return time / 20.0
        else:
            return time / 25.0
    else:
        if white_pieces_count < black_pieces_count:
            if count_set_bits(board.queens & board.black_pieces) == 1 or \
                    count_set_bits(board.bishops & board.black_pieces) == 1 or \
                    count_set_bits(board.rooks & board.black_pieces) == 1:
                return time / 10.0
            return time / 20.0
        else:
            return time / 25.0


def count_set_bits(binary_number):
    # Zähle die Anzahl der Einsen (gesetzte Bits) in der binären Darstellung einer Zahl
    return bin(binary_number).count("1")