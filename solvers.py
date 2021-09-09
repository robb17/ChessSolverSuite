import chess
from itertools import permutations
import random
import math
import argparse
import time
from copy import deepcopy

class MiniMaxSolver:
	def __init__(self, size, filename, aggressor):
		self.game = chess.Game(size, filename, aggressor)
		self.size = size

	def solve(self):
		return self.board

class AlphaBetaSolver:
	def __init__(self, size, filename):
		self.board = chess.Board(size, filename)
		self.size = size

	def solve(self):
		
		return self.board

class TranspositionSolver:
	def __init__(self, size, filename):
		self.board = chess.Board(size, filename)
		self.size = size

	def solve(self):
		
		return self.board


def average(lst):
	acc = 0
	for i in lst:
		acc += i
	return (acc / len(lst))

if __name__ == "__main__":
	types = {
			"minimax": [MiniMaxSolver],
			"alphabeta": [AlphaBetaSolver],
			"transposition": [TranspositionSolver]
			}
	types["all"] = list(types.values())
	types_keys = list(types.keys())
	formatted_types = "".join(x + ", " for x in types_keys[:-1])
	formatted_types += types_keys[-1]

	parser = argparse.ArgumentParser(description='Determine a sequence of moves to put an opponent in checkmate')
	parser.add_argument('size', metavar='S', help='the size of the chess board', type=int)
	parser.add_argument('type', metavar='T', nargs="*", help='select the type of method used in finding a \
			solution. Available types:' + formatted_types, default="all", choices=types_keys)
	parser.add_argument('-l', "--load", help='load a file containing a representation of \
			the ' + "board's" + ' starting state.')
	parser.add_argument('-a', "--aggressor", help='indicate which player should go first', default=chess.PLAYER1, choices=[chess.PLAYER1, chess.PLAYER2])
	args = parser.parse_args()

	if isinstance(args.type, str):
		args.type = [args.type]
	all_times_1 = []
	all_times_2 = []
	if not args.load:
		print("An initial board state is required.")
		exit(1)
	for t in args.type:
		for c in types[t]:
			t1 = time.time()
			instance = c(args.size, args.load, args.aggressor)
			board = instance.solve()
			print(board)
			print("Finished in " + str(round(time.time() - t1, 2)) + " seconds")

