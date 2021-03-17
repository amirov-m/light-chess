#!/usr/bin/python3

import unittest

from engine.game import Game
from engine.piece_moves import PieceMoves
from entities.board import Board
from entities.colour import Colour
from entities.move import Move
from entities.pieces import Pieces
from entities.position import Position
from entities.possible_castle import PossibleCastle


class TestPieceMoves(unittest.TestCase):
    """Test of PieceMoves class.
    Create dummy board by means of setUp() method and check the correctness of pieces moves.
    """

    def setUp(self) -> None:
        """Creates dummy game."""

        self.board = Board()
        self.board.set_piece(Position(4, 0), Pieces.WHITE_KING)
        self.board.set_piece(Position(0, 0), Pieces.WHITE_ROOK)
        self.board.set_piece(Position(0, 1), Pieces.WHITE_PAWN)
        self.board.set_piece(Position(7, 0), Pieces.WHITE_ROOK)
        self.board.set_piece(Position(7, 1), Pieces.WHITE_PAWN)
        self.board.set_piece(Position(4, 4), Pieces.WHITE_PAWN)

        self.board.set_piece(Position(2, 7), Pieces.BLACK_ROOK)
        self.board.set_piece(Position(3, 4), Pieces.BLACK_PAWN)
        self.board.set_piece(Position(5, 4), Pieces.BLACK_PAWN)

        self.game = Game(self.board, Colour.WHITE, PossibleCastle(), Position(3, 5))

    def test_castling_moves(self):
        """Test of castling_moves() method."""

        assert sorted(PieceMoves.castling_moves(Position(4, 0), self.game)) == [
            Move(Position(4, 0), Position(6, 0))
        ]

    def test_pawn_moves(self):
        """Test of pawn_moves() method."""
        print(sorted(PieceMoves.pawn_moves(Position(4, 4), self.game)))
        assert sorted(PieceMoves.pawn_moves(Position(4, 4), self.game)) == [
            Move(Position(4, 4), Position(3, 5)),
            Move(Position(4, 4), Position(4, 5)),
        ]

    def test_king_moves(self):
        """Test of king_moves() method."""

        assert sorted(PieceMoves.king_moves(Position(4, 0), self.game)) == [
            Move(Position(4, 0), Position(3, 0)),
            Move(Position(4, 0), Position(3, 1)),
            Move(Position(4, 0), Position(4, 1)),
            Move(Position(4, 0), Position(5, 0)),
            Move(Position(4, 0), Position(5, 1)),
            Move(Position(4, 0), Position(6, 0)),
        ]

    def test_all_moves(self):
        """Test of all_moves() method."""
        assert sorted(PieceMoves.all_moves(self.game)) == [
            Move(Position(0, 0), Position(1, 0)),
            Move(Position(0, 0), Position(2, 0)),
            Move(Position(0, 0), Position(3, 0)),
            Move(Position(0, 1), Position(0, 2)),
            Move(Position(0, 1), Position(0, 3)),
            *sorted(PieceMoves.king_moves(Position(4, 0), self.game)),
            Move(Position(4, 4), Position(3, 5)),
            Move(Position(4, 4), Position(4, 5)),
            Move(Position(7, 0), Position(5, 0)),
            Move(Position(7, 0), Position(6, 0)),
            Move(Position(7, 1), Position(7, 2)),
            Move(Position(7, 1), Position(7, 3)),
        ]
