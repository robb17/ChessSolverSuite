from math import inf
from association_table import AssociationTable
from coordinates import X, Y, invalid_coordinates

STRAIGHT = 0
DIAGONAL = 1
L = 2

KING = 0b0
QUEEN = 0b1
ROOK = 0b10
KNIGHT = 0b11
BISHOP = 0b100
PAWN = 0b101
NONE = 0b110
MARKED_NULL = 0b111

BOARD = 0
PLAYER1 = 1
PLAYER2 = 2

class ThreatPattern:
	def __init__(self, pattern_string, distance):
		self.pattern_string = pattern_string
		self.distance = distance

	def is_threatening(self, starting_x, starting_y, x, y):
		if starting_x == x and starting_y == y:
			return False
		if self.pattern_string == STRAIGHT:
			return (starting_x == x and self.distance >= abs(starting_x - x)) or (starting_y == y and self.distance >= abs(starting_y - y))
		elif self.pattern_string == DIAGONAL:
			return abs((y - starting_y) / (x - starting_x)) == 1 and self.distance >= abs(y - starting_y)
		elif self.pattern_string == L:
			return (abs(x - starting_x) == 1 and abs(y - starting_y) == 2) or (abs(x - starting_x) == 2 and abs(y - starting_y) == 1)
		elif self.pattern_string == NONE:
			return False

	def all_threatened_locations(self, x, y, size):
		''' Gives all threatened locations for x' in 0 < x' < size 
			and y' in 0 < y' < size
		'''
		locations = []
		if self.pattern_string == STRAIGHT:
			x_temp = 0
			while x_temp < size:
				if x_temp != x:
					locations.append((x_temp, y))
				x_temp += 1
			y_temp = 0
			while y_temp < size:
				if y_temp != y:
					locations.append((x, y_temp))
				y += 1
		elif self.pattern_string == DIAGONAL:
			x_temp = 0 if x < y else x - y
			y_temp = 0 if x > y else y - x
			x_temp2 = 0 if x + y <= size else x + y - size
			y_temp2 = size - 1 if x + y >= size else x + y
			while x_temp2 < size and y_temp2 >= 0:
				if x_temp_2 != x:
					locations.append((x_temp2, y_temp2))
				x_temp2 += 1
				y_temp2 -= 1
			while x_temp < size and y_temp < size:
				if x_temp != x:
					locations.append((x_temp, y_temp))
				x_temp += 1
				y_temp += 1
		elif self.pattern_string == L:
			dx = [1, -1, 2, -2, 1, -1, 2, -2]
			dy = [2, 2, 1, 1, -2, -2, -1, -1]
			for i in range(0, len(dx)):
				if dx[i] + x >= 0 and dx[i] + x < size and dy[i] + y >= 0 and dy[i] + y < size:
					locations.append((dx[i] + x, dy[i] + y))
		return locations

ALL_PATTERNS = {
	KING: [ThreatPattern(STRAIGHT, 1), ThreatPattern(DIAGONAL, 1)],
	QUEEN: [ThreatPattern(STRAIGHT, inf), ThreatPattern(DIAGONAL, inf)],
	ROOK: [ThreatPattern(STRAIGHT, inf)],
	KNIGHT: [ThreatPattern(L, None)],
	BISHOP: [ThreatPattern(DIAGONAL, inf)],
	PAWN: [ThreatPattern(DIAGONAL, 1)],
	NONE: [ThreatPattern(NONE, None)]
	}

ALL_REPRESENTATIONS = AssociationTable({	# support bidirectional indexing
	KING: "K",
	QUEEN: "Q",
	ROOK: "R",
	KNIGHT: "K",
	BISHOP: "B",
	PAWN: "P",
	NONE: "-",
	MARKED_NULL: "!"
})

class Piece:
	def __init__(self, x, y, board, player, type=""):
		self.x = x
		self.y = y
		self.threat_patterns = ALL_PATTERNS[type]
		self.type = type
		self.threats = {}
		self.board = board
		self.player = player

	def is_threatening(self, x, y):
		for pattern in self.threat_patterns:
			if pattern.is_threatening(self.x, self.y, x, y):
				return True
		return False

	def is_threatened_by_opponent(self):
		opponent = self.player.get_opponent()
		if opponent:
			for threatening_piece in self.threats:
				if not threatening_piece.is_same_team(opponent):
					return True
		return False

	def add_threat(self, piece):
		self.threats[piece] = True

	def remove_threat(self, piece):
		self.threats.pop(piece)

	def all_threatened_locations(self, x, y):
		locations = []
		for pattern in self.threat_patterns:
			locations += pattern.all_threatened_locations(x, y, self.board.size)
		return locations

	def is_same_team(self, player):
		return self.player == player

	def all_moves(self):
		all_moves = self.all_threatened_locations(x, y, self.board.size)
		if self.type == KING:
			all_moves_temp = []
			for move in all_moves:
				if not self.board[move[X]][move[Y]].is_threatened_by_opponent()
					all_moves_temp.append(move)
			all_moves = all_moves_temp
		final_moves = []
		for move in all_moves:
			if not self.board[move[X]][move[Y]].is_same_team(self.player):
				final_moves.append(move)
		return final_moves

	def __str__(self):
		#if self.type == NONE and len(self.threats) > 0:
		#	return ALL_REPRESENTATIONS[MARKED_NULL]
		return ALL_REPRESENTATIONS[self.type]

	def __int__(self):
		''' 0b0 ... 0b110 for P1, 0b1000 to 0b1110 for P2
		'''
		return self.type if self.player.number == PLAYER1 else 8 + self.type

	def __hash__(self):
		return self.x * 10000 + self.y

class King(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, KING)

class Queen(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, QUEEN)

class Rook(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, ROOK)

class Knight(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, KNIGHT)

class Bishop(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, BISHOP)

class Pawn(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, PAWN)

class Dummy(Piece):
	def __init__(self, x, y, player, board):
		super().__init__(x, y, board, player, NONE)

class Player:
	''' Players' pieces are defined as non-dummy pieces
	'''
	def __init__(self, number, board):
		self.pieces = {}
		self.number = number
		self.board = board
		self.king = None

	def all_pieces(self):
		return self.pieces

	def move_piece(self, piece, coordinates):
		target_piece = self.board[coordinates[X]][coordinates[Y]]
		self.remove_piece(target_piece)
		self.remove_piece(piece)
		piece.x = coordinates[X]
		piece.y = coordinates[Y]
		self.add_piece(piece)

	def add_piece(self, piece, mark_new_threats=False):
		self.pieces[piece] = piece
		if len(self.board) == self.board.size:	# only add piece if board is already initialized
			self.board[piece.x][piece.y] = piece
		self.board.add_threats(piece.all_threatened_locations(piece.x, piece.y), piece)
		if piece.type == KING:
			if self.king:
				print("Invalid board: multiple kings")
				exit(1)
			self.king = piece

	def remove_piece(self, piece):
		self.pieces.pop(piece)
		self.board[piece.x][piece.y] = Dummy(piece.x, piece.y, self, self.board)
		self.board.remove_threats(piece.all_threatened_locations(piece.x, piece.y), piece)

	def all_moves(self):
		all_moves = {}
		for piece in self.pieces.values():
			all_moves[piece] = piece.all_moves()
		return all_moves

	def is_in_checkmate(self):
		if self.king and len(self.king.all_moves()) == 0 and self.king.is_threatened_by_opponent():
			return True
		else:
			return False

	def is_in_stalemate(self):
		if self.king and len(self.king.all_moves()) == 0 and not self.king.is_threatened_by_opponent():
			return True
		else:
			return False

	def get_opponent(self):
		if self.number == BOARD:
			return None
		return PLAYER1 if self.number == PLAYER2 else PLAYER2

class Board:
	def __init__(self, size, game, filename):
		self.size = size
		self.game = game
		self._load_from_file(filename)

	def _load_from_file(self, filename):
		self.board = []
		row = []
		x = 0
		y = 0
		self.size = None
		with open(filename, "r") as rep:
			for line in rep:
				for c in line:
					if c == " ":
						continue
					elif ALL_REPRESENTATIONS.get(c.upper()):
						player_number = PLAYER1 if c.is_lower() else PLAYER2
						player = self.game.player(BOARD) if c == ALL_REPRESENTATIONS[NONE] else self.game.player(player_number)
						piece = Piece(x, y, self, player, ALL_REPRESENTATIONS[c.upper()])
						if ALL_REPRESENTATIONS[c.upper()] != NONE and ALL_REPRESENTATIONS[c.upper()] != MARKED_NULL:
							self.game.player(player_number).add_piece(piece)
						row.append(piece)
						y += 1
				self.board.append(row)
				row = []
				if not self.size:
					self.size = y
				elif y != self.size:
					print("Malformed board: variable width")
					exit(1)
				x += 1
				y = 0
			if not ((x == self.size and y == 0) or (x == self.size - 1 and y == self.size - 1)):
				print("Malformed board: height does not match width")
				exit(1)
		print("Load complete")
		print(self)

	def all_pieces(self):
		return self.game.player(PLAYER1).all_pieces().update(self.game.players(PLAYER2).all_pieces())

	def determine_threats(self):
		for theatened_piece in self.all_pieces():
			for piece in self.all_pieces():
				if piece.is_threatening(theatened_piece.x, theatened_piece.y):
					theatened_piece.add_threat(piece)

	def add_threats(self, locations, threatening_piece):
		for location in locations:
			self.board[location[X]][location[Y]].add_threat(threatening_piece)

	def remove_threats(self, locations, threatening_piece):
		for location in locations:
			if threatening_piece.is_threatening(location[0], location[1]):
				self.board[location[X]][location[Y]].remove_threat(threatening_piece)

	def is_position_threatened_by_opponent(self, x, y):
		return self.board[x][y].is_threatened_by_opponent()

	def get_value(self):
		if self.game.player(PLAYER1).is_in_checkmate():
			return -1
		elif self.game.player(PLAYER2).is_in_checkmate():
			return 1
		else:
			return 0

	def __str__(self):
		string_rep = "\n"
		for row in self.board:
			for piece in row:
				string_rep += str(piece) + " "
			string_rep += "\n"
		return string_rep

	def __setitem__(self, x, val):
		self.board[x] = val

	def __getitem__(self, x):
		return self.board[x]

	def __len__(self):
		return self.size

	def __hash__(self):
		hsh = 0
		for x in range(0, self.size):
			for y in range(0, self.size):
				hsh = hsh << 4
				hsh += int(self.board[x][y])
		return hsh

class Game:
	def __init__(self, size, filename, aggressor):
		self.board = Board(size, self, filename)
		self.players = {BOARD: Player(BOARD, self.board), PLAYER1: Player(PLAYER1, self.board), PLAYER2: Player(PLAYER2, self.board)}
		self.aggressor = self.players[aggressor]

	def player(self, player_number):
		return self.players.get(player_number)

	def all_players(self):
		return [player for player in self.players.values() if player.number != BOARD]

	def to_move(self):
		return self.aggressor

	def make_move(self, init_coordinates, end_coordinates):
		if invalid_coordinates(init_coordinates, self.board.size) or invalid_coordinates(end_coordinates, self.board.size)\
				or self.board[init_coordinates[X]][init_coordinates[Y]].player != self.aggressor \
				or self.board[end_coordinates[X]][end_coordinates[Y]].player == self.aggressor:
			print("Illegal move requested:", init_coordinates, "to", end_coordinates)
			return False

		init_piece = self.board[init_coordinates[X]][init_coordinates[Y]]

		self.aggressor.move_piece(init_piece, end_coordinates)

		self.aggressor = PLAYER1 if self.aggressor == PLAYER2 else PLAYER2
		return True
