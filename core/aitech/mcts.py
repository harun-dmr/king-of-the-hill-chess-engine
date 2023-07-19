"""

Mote Carlo Tree Search

"""

import time
import copy
import random

import numpy as np
import multiprocessing as mp

from core.utils import Board, Move
from core.zuggenerator import generate, random_legal_move, game_ending
from core.zuggenerator import check_for_checkmate, check_king_hill, gen_all_masks
from core.zuggenerator import rook_moves, bishop_moves, pawn_moves


ROOT_TWO = 1.4142


class Node():
    def __init__(self, board, parent = None, move = None, terminal = False):
        self.wins = 0
        self.simulations = 0
        self.children = []
        self.board = board
        self.parent = parent
        self.move = move
        self.terminal = terminal
        self.rest_moves = []

    @property
    def value(self):
        if self.simulations == 0 or self.wins == 0:
            return 0
        calc = (self.wins / self.simulations) + ROOT_TWO * np.sqrt(np.abs(np.log(self.parent.simulations) / self.simulations))

        return calc

    def __eq__(self, other):
        # THIS ONLY COMPARES THE MOVES THAT LED TO THIS NODE!
        return self.move == other.move


    def __repr__(self):
        return f"wins: {self.wins}, simulation: {self.simulations}, value: {self.value}, terminal: {self.terminal}, move: {self.move}"



class MctsInstance():
    def __init__(self):
        #super(MctsInstance, self).__init__(args=[board, moves])
        self.first_children: [Node] = []
        self.time_to_stop = 0
        #self.run(board, moves)
        self.move_count = 0

    def run(self, board: Board = None, moves: Move = None):
        gen_all_masks()
        #print(board)
        if moves is None:
            moves = generate(board)

        root = Node(board, parent=None, move=None, terminal=game_ending(board))
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.do_move(move)
            self.first_children.append(Node(new_board, parent=root, move=move, terminal=game_ending(board)))
        root.children = self.first_children
        #self.first_children = [Node(board, parent=None, move=move, terminal=game_ending(board)) for move in moves]

        #print(time.time())
        #print(self.time_to_stop)
        simulated_games = 0
        while time.time() < self.time_to_stop:
            leaf = self.traverse()
            if not leaf: continue
            sim_res = self.simulate(leaf)
            if not sim_res: continue
            self.backpropagate(sim_res)
            simulated_games += 1

        #print(root.simulations)
        move, score = self.choose_move()
        #print(f"Best Move: {move}")
        #print(self.first_children)
        #print(self.move_count)
        return move, score, simulated_games

    def choose_move(self):
        node = max(self.first_children, key=lambda x: x.value)
        return node.move, node.value





    def random_move(self, board) -> (Move, Board):
        if board.active_color:
            active_pieces = board.white_pieces
        else:
            active_pieces = board.black_pieces
        rand_num = random.randint(0, 5)
        random_piece = board.boards[rand_num] & active_pieces
        if random_piece == 0:
            for i in range(5):
                rand_num = random.randint(0, 5)
                random_piece = board.boards[rand_num] & active_pieces
                if random_piece != 0:
                    break
            if random_piece == 0:
                moves = generate(board)
                return random.choice(moves)


    def traverse(self):
        return random.choice(self.first_children)

    def simulate(self, leaf):
        leaf.terminal = game_ending(leaf.board)

        for i in range(300):
            if leaf.terminal:
                return leaf
            move, new_board = random_legal_move(leaf.board, iterations=5)
            if not move:
                move = random.choice(generate(leaf.board))
                new_board = copy.deepcopy(leaf.board)
                new_board.do_move(move)
            new_node = Node(new_board, parent=leaf, move=move, terminal=game_ending(new_board))
            if new_node in leaf.children:
                #print("Node was already a child")
                leaf = leaf.children[leaf.children.index(new_node)]
            else:
                self.move_count += 1
                leaf.children.append(new_node)
            leaf = new_node

        #print("here")
        return False

    def traverse_gen_all_moves(self):
        pick = random.choice(self.first_children)
        depth = 1
        for i in range(20):
            if pick.terminal:
                return False
            if not pick.children and not pick.rest_moves:
                pick.rest_moves = generate(pick.board)
            if pick.rest_moves:
                move = random.choice(pick.rest_moves)
                new_board = copy.deepcopy(pick.board)
                new_board.do_move(move)
                node = Node(new_board, parent=pick, move=move)
                pick.children.append(node)
                return node

            #print(pick, depth)
            pick = random.choice(pick.children)


        return False


    def simulate_gen_all_moves(self, leaf):
        leaf.terminal = game_ending(leaf.board)

        for i in range(200):
            if leaf.terminal:
                return leaf
            leaf.rest_moves = generate(leaf.board)
            move = random.choice(leaf.rest_moves)
            new_board = copy.deepcopy(leaf.board)
            new_board.do_move(move)
            new_node = Node(new_board, parent=leaf, move=move, terminal=game_ending(new_board))
            leaf.children.append(new_node)
            leaf = new_node

        return False

    def backpropagate(self, leaf):
        # wining color
        wc = None
        if check_for_checkmate(leaf.board) or check_king_hill(leaf.board):
            wc = leaf.board.active_color
        else:
            wc = not leaf.board.active_color

        node = leaf
        while node is not None:
            node.simulations += 1
            if node.board.active_color == wc:
                node.wins += 1
            node = node.parent

        return


def worker(args):
    gen_all_masks()
    board, moves, stop_time = args
    p = MctsInstance()
    p.time_to_stop = stop_time
    return p.run(board, moves)


def mcts(board: Board, time_limit):

    stop_time = time.time() + time_limit

    cpus = mp.cpu_count()

    moves = generate(board)
    moves_pp = len(moves) // (cpus - 1)
    if moves_pp < 1:
        moves_list = [moves]
    else:
        moves_list = [moves[i:i + moves_pp] for i in range(0, len(moves), moves_pp)]

    argsp = [(board, moves, stop_time) for moves in moves_list]

    with mp.Pool(processes=cpus) as pool:
        res = pool.map(worker, argsp)

    #print(res)

    highscore = 0
    best_move = None
    games = 0

    for move, score, gs in res:
        if highscore < score:
            highscore = score
            best_move = move
        games += gs

    print(f"Games simulated: {games}")

    #print("")
    #print(f"BEST MOVE OF ALL: {best_move}")
    return move





if __name__ == "__main__":
    #gen_all_masks()
    gen_all_masks()
    fen = "r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w - - 0 1"
    board = Board(fen)
    best_move = mcts(board, 10)
    print(best_move)



    #moves = generate(board)

    #p = MctsInstance(board, moves)
    #p.time_to_stop = time.time() + 10
    #print(p.time_to_stop)
    #res = p.run(board, moves)
    #print(res)
    #p.start()
    #p.join()
    #p.close()