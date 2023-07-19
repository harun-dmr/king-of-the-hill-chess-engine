import numpy as np


STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

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

class Move:
    """
    This class Represents a Move on a Board
    """
    def __init__(self, origin: int = None, target: int = None, capture: bool = None, promotion: int = None, castle = None, piece: int = None):
        self.origin = origin
        self.target = target
        self.capture = capture
        self.promotion = promotion

        self.castle = castle
        self.piece = piece

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.origin == other.origin and self.target == other.target and self.capture == other.capture and self.promotion == other.promotion and self.castle == other.castle and self.piece == other.piece
        return False

    def __hash__(self):
        return hash((self.origin, self.target, self.capture, self.promotion, self.castle, self.piece))

    def __repr__(self):
        #return ""
        row = ["a","b","c","d","e","f","g","h"]
        lsb_origin = (get_lsb(self.origin))
        eins = 0
        zwei = 7
        for r in range (8):
            o = 0
            for r1 in range(eins,zwei+1):
                if 2**(r1) == lsb_origin:
                    s = str(8-r)
                    move = row[o]+""+s
                o = o+1
            eins = r1+1
            zwei = eins+7 
        
        lsb_target = (get_lsb(self.target))
        eins = 0
        zwei = 7
        for r in range (8):
            o = 0
            for r1 in range(eins,zwei+1):
                if 2**(r1) == lsb_target:
                    s = str(8-r)
                    target = row[o]+""+s
                o = o+1
            eins = r1+1
            zwei = eins+7 
        
        richtung = "->"
        if self.capture: richtung="x"

        return move + target
        #return "Move:\n" + '\n'.join([np.binary_repr(self.origin, width=64)[i:i + 8] for i in range(0, 64, 8)]) + "\n target\n" + '\n'.join([np.binary_repr(self.target, width=64)[i:i + 8] for i in range(0, 64, 8)]) + "\n"



class Board():
    """
    This Class represents a Board
    It also acts as a Gamestate.
    """
    _translation = {
        6: '♚',
        5: '♛',
        4: '♜',
        3: '♝',
        2: '♞',
        1: '♟︎',
        12: '♔',
        11: '♕',
        10: '♖',
        9: '♗',
        8: '♘',
        7: '♙',
    }

    def __init__(self, fen=None):

        self.active_color: bool

        self.castling_wk: bool
        self.castling_wq: bool
        self.castling_bk: bool
        self.castling_bq: bool

        self.moves: list


        if fen is not None:
            fields = fen_split(fen)
            self.active_color = fields[1] == 'w'

            # set castling availability
            self.castling_wk = 'K' in fields[2]
            self.castling_wq = 'Q' in fields[2]
            self.castling_bk = 'k' in fields[2]
            self.castling_bq = 'q' in fields[2]

            self.boards = fen_to_bitboards(fen)

            self.moves = None
        else:
            self.boards = [None for _ in range(8)]
            self.moves = None

    def __deepcopy__(self, memodict={}):
            b = Board()
            b.active_color = self.active_color

            b.castling_wq = self.castling_wq
            b.castling_wk = self.castling_wk
            b.castling_bk = self.castling_bk
            b.castling_bq = self.castling_bq

            b.boards = [x for x in self.boards]
            if self.moves is not None:
                b.moves = [x for x in self.moves]

            return b

    @property
    def pawns(self):
        return self.boards[0]

    @property
    def knights(self):
        return self.boards[1]

    @property
    def bishops(self):
        return self.boards[2]

    @property
    def rooks(self):
        return self.boards[3]

    @property
    def queens(self):
        return self.boards[4]

    @property
    def kings(self):
        return self.boards[5]

    @property
    def black_pieces(self):
        return self.boards[6]

    @property
    def white_pieces(self):
        return self.boards[7]

    def __repr__(self):
        board = [['\u2003'] * 8 for _ in range(8)]
        for x in range(6):
            number = self.boards[7] & self.boards[x]
            while number != 0:
                number, lsb = pop_lsb(number)
                position = get_first_set_bit_position(lsb)
                row, col = divmod(position-1, 8)
                board[row][col] = self._translation.get(x + 7)

        for x in range(6):
            number = self.boards[6] & self.boards[x]
            while number != 0:
                number, lsb = pop_lsb(number)
                position = get_first_set_bit_position(lsb)
                row, col = divmod(position-1, 8)
                board[row][col] = self._translation.get(x + 1)

        # Add border lines and labels
        board_str = "  a b c d e f g h\n"
        for i in range(8):
            row_str = f"{8 - i} " + " ".join(str(cell) for cell in board[i]) + f" {8 - i}\n"
            board_str += row_str
        board_str += "  a b c d e f g h\n"

        return board_str

    def __iter__(self):
        for board in self.boards:
            yield board

    def __hash__(self):
        return hash((tuple(self.boards), self.castling_wk, self.castling_bk, self.castling_wq, self.castling_wq, self.active_color))


    def do_move(self, move: Move):
        """
        Changes Bitboards acording to Move.
        Changes active color.

        :param move: The move to be executed
        :return: nothing
        """

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

        # pawn promotion --> set bitboards of new piece
        if move.promotion is not None:
            # change bitboards of captured piece
            if move.capture is not None:
                for i in range(len(self.boards)):
                    if self.boards[i] & move.target:
                        self.boards[i] = self.boards[i] & ~move.target
            nbitboard.get(move.promotion)[0] = nbitboard.get(move.promotion)[0] | move.target
            nbitboard.get(move.promotion)[1] = nbitboard.get(move.promotion)[1] | move.target
            # change bitboards of moved piece
            for i in range(len(self.boards)):
                if self.boards[i] & move.origin:
                    self.boards[i] = self.boards[i] & ~move.origin
            # change turns
            self.active_color = not self.active_color
            return
        elif move.castle is not None:
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

        # change bitboards of moved piece
        for i in range(len(self.boards)):
            if self.boards[i] & move.origin:
                self.boards[i] = self.boards[i] & ~move.origin
                self.boards[i] = self.boards[i] | move.target

        # change turns
        self.active_color = not self.active_color
        self.moves = None

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

def get_first_set_bit_position(number):
    # Konvertiere die Zahl in eine Binärzahl und entferne das Präfix '0b'
    binary_string = bin(number)[2:]

    # Invertiere die Binärzahl, um das Zählen von rechts zu starten
    inverted_string = binary_string[::-1]

    # Suche nach der ersten '1' und gib ihre Position zurück
    position = inverted_string.find('1')

    # Beachte, dass die Positionen bei 0 beginnen, daher wird 1 addiert
    return position + 1 if position != -1 else -1


def fen_split(fen):
    fen_parts = fen.split()
    board_state = fen_parts[0]
    active_color = fen_parts[1]
    castling = fen_parts[2]
    en_passant = fen_parts[3]
    half_move_clock = fen_parts[4]
    full_move_number = fen_parts[5]

    return fen_parts


def fen_to_bitboards(fen):
    # Initialize bitboards
    pawns, knights, bishops, rooks, queens, kings = 0, 0, 0, 0, 0, 0
    black_pieces, white_pieces = 0, 0

    # Split FEN string into individual parts
    fen_parts = fen_split(fen)
    board_state = fen_parts[0]

    # Convert board state to 8 bitboards
    ranks = board_state.split('/')
    for i in range(8):
        file_index = 0
        for char in ranks[i]:
            if char.isdigit():
                file_index += int(char)
            else:
                # Calculate bit position
                bit_position = i * 8 + file_index
                # Determine piece type
                if char == 'P':
                    pawns |= (1 << bit_position)
                    white_pieces |= (1 << bit_position)
                elif char == 'N':
                    knights |= (1 << bit_position)
                    white_pieces |= (1 << bit_position)
                elif char == 'B':
                    bishops |= (1 << bit_position)
                    white_pieces |= (1 << bit_position)
                elif char == 'R':
                    rooks |= (1 << bit_position)
                    white_pieces |= (1 << bit_position)
                elif char == 'Q':
                    queens |= (1 << bit_position)
                    white_pieces |= (1 << bit_position)
                elif char == 'K':
                    kings |= (1 << bit_position)
                    white_pieces |= (1 << bit_position)
                elif char == 'p':
                    pawns |= (1 << bit_position)
                    black_pieces |= (1 << bit_position)
                elif char == 'n':
                    knights |= (1 << bit_position)
                    black_pieces |= (1 << bit_position)
                elif char == 'b':
                    bishops |= (1 << bit_position)
                    black_pieces |= (1 << bit_position)
                elif char == 'r':
                    rooks |= (1 << bit_position)
                    black_pieces |= (1 << bit_position)
                elif char == 'q':
                    queens |= (1 << bit_position)
                    black_pieces |= (1 << bit_position)
                elif char == 'k':
                    kings |= (1 << bit_position)
                    black_pieces |= (1 << bit_position)
                file_index += 1

    # Return bitboards as a tuple
    return [pawns, knights, bishops, rooks, queens, kings, black_pieces, white_pieces]


def get_empty_squares_bitboard(fen):
    """
    Returns a bitboard with empty squares represented by 1's and occupied squares by 0's.
    """
    # Get the bitboards for the team and opposing color pieces
    bitboards = fen_to_bitboards(fen)
    team_color_bitboard = bitboards[-2 if fen.split()[1] == 'w' else -1]
    opposing_color_bitboard = bitboards[-1 if fen.split()[1] == 'w' else -2]

    # Return the bitwise OR of the team and opposing color bitboards, inverted
    return ~(team_color_bitboard | opposing_color_bitboard) & 0xFFFFFFFFFFFFFFFF


def print_bitboards(fen):
    bitboards = fen_to_bitboards(fen)
    print("Pawns:")
    print('\n'.join([np.binary_repr(bitboards[0], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("Knights:")
    print('\n'.join([np.binary_repr(bitboards[1], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("Bishops:")
    print('\n'.join([np.binary_repr(bitboards[2], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("Rooks:")
    print('\n'.join([np.binary_repr(bitboards[3], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("Queens:")
    print('\n'.join([np.binary_repr(bitboards[4], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("Kings:")
    print('\n'.join([np.binary_repr(bitboards[5], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("Black Pieces:")
    print('\n'.join([np.binary_repr(bitboards[6], width=64)[i:i + 8] for i in range(0, 64, 8)]))
    print("White Pieces:")
    print('\n'.join([np.binary_repr(bitboards[7], width=64)[i:i + 8] for i in range(0, 64, 8)]))


def print_bitboard(board: int):
    print('\n'.join([np.binary_repr(board, width=64)[i:i + 8] for i in range(0, 64, 8)]))


if __name__ == "__main__":
    fen = "8/qk1N4/3r4/8/8/3R4/QK6/8 w - - 0 1"
    boards = fen_to_bitboards(fen)
    board = Board(fen)
    print(board)
