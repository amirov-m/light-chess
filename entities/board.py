#!/usr/bin/python3

from __future__ import annotations

from collections import defaultdict

from .pieces import Piece, PieceType, PieceColour
from .position import Position
from typing import List, Optional

class Board(object):
	"""
	Represents a chess board.
	"""

	def __init__(self) -> None:
		# Stores mapping from unique pairs of (piece_type, piece_pos)
		# to a set of positions.
		# Used for getting all positions for a specific piece type.
		self._piece_to_pos = defaultdict(set)
		# Stores mapping from position to a piece description.
		# Used for getting a piece standing on a position.
		self._pos_to_piece = dict()

	# Set a provided piece on a specified position.
	def set_piece(self, pos: Position, piece: Piece) -> None:
		self.remove_piece(pos)

		self._piece_to_pos[piece].add(pos)
		self._pos_to_piece[pos] = piece

	# Return a piece on a specified position.
	# 
	# Method returns None if there is no piece on a specified position.
	def get_piece(self, pos) -> Optional[Piece]:
		return self._pos_to_piece.get(pos)

	# Remove piece from a specified position.
	#
	# If there is no piece on a specified position, do nothig.
	def remove_piece(self, pos) -> None:
		piece_to_remove = self._pos_to_piece.get(pos)
		if piece_to_remove is not None:
			self._piece_to_pos[piece_to_remove].remove(pos)
			del self._pos_to_piece[pos]

	# Return the position of a specific piece.
	#
	# If several or 0 positions were found, throw SinglePositionNotFoundError.
	def get_single_piece_position(self, piece) -> Position:
		pass

	# Return positions of a specific piece.
	def get_positions_for_piece(self, piece: Piece) -> List[Position]:
		return list(self._piece_to_pos[piece])

	# Create a chess board with a default start position.
	@staticmethod
	def create_start_board() -> Board:
		board = Board()

		# Set white pieces.
		board.set_piece(Position(0, 0), Piece(PieceType.Rook, PieceColour.White))
		board.set_piece(Position(1, 0), Piece(PieceType.Knight, PieceColour.White))
		board.set_piece(Position(2, 0), Piece(PieceType.Bishop, PieceColour.White))
		board.set_piece(Position(3, 0), Piece(PieceType.Queen, PieceColour.White))
		board.set_piece(Position(4, 0), Piece(PieceType.King, PieceColour.White))
		board.set_piece(Position(5, 0), Piece(PieceType.Bishop, PieceColour.White))
		board.set_piece(Position(6, 0), Piece(PieceType.Knight, PieceColour.White))
		board.set_piece(Position(7, 0), Piece(PieceType.Rook, PieceColour.White))

		board.set_piece(Position(0, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(1, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(2, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(3, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(4, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(5, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(6, 1), Piece(PieceType.Pawn, PieceColour.White))
		board.set_piece(Position(7, 1), Piece(PieceType.Pawn, PieceColour.White))


		# Set black pieces.
		board.set_piece(Position(0, 7), Piece(PieceType.Rook, PieceColour.Black))
		board.set_piece(Position(1, 7), Piece(PieceType.Knight, PieceColour.Black))
		board.set_piece(Position(2, 7), Piece(PieceType.Bishop, PieceColour.Black))
		board.set_piece(Position(3, 7), Piece(PieceType.Queen, PieceColour.Black))
		board.set_piece(Position(4, 7), Piece(PieceType.King, PieceColour.Black))
		board.set_piece(Position(5, 7), Piece(PieceType.Bishop, PieceColour.Black))
		board.set_piece(Position(6, 7), Piece(PieceType.Knight, PieceColour.Black))
		board.set_piece(Position(7, 7), Piece(PieceType.Rook, PieceColour.Black))

		board.set_piece(Position(0, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(1, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(2, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(3, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(4, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(5, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(6, 6), Piece(PieceType.Pawn, PieceColour.Black))
		board.set_piece(Position(7, 6), Piece(PieceType.Pawn, PieceColour.Black))

		return board