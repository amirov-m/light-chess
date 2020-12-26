#!/usr/bin/python3

import unittest
from entities.board import Board
from entities.position import Position
from entities.pieces import Piece
from entities.pieces import PieceType
from entities.colour import Colour
from entities.move import Move
from engine.logic import GameLogic
from engine.game import Game


class TestGameLogic(unittest.TestCase):
    """Test of GameLogic class.
        Create dummy gsme by means of setUp() method and check the correctness of pieces moves.
    """

    def setUp(self) -> None:
        """Create dummy game.
        """

        # Create dummy board
        self.board = Board()
        self.board.set_piece(Position(4, 0), Piece(PieceType.King, Colour.WHITE))
        self.board.set_piece(Position(0, 0), Piece(PieceType.Rook, Colour.WHITE))
        self.board.set_piece(Position(7, 0), Piece(PieceType.Rook, Colour.WHITE))
        self.board.set_piece(Position(4, 4), Piece(PieceType.Pawn, Colour.WHITE))
        self.board.set_piece(Position(4, 1), Piece(PieceType.Bishop, Colour.WHITE))

        self.board.set_piece(Position(3, 4), Piece(PieceType.Pawn, Colour.BLACK))
        self.board.set_piece(Position(5, 4), Piece(PieceType.Pawn, Colour.BLACK))
        self.board.set_piece(Position(4, 3), Piece(PieceType.Rook, Colour.BLACK))
        self.board.set_piece(Position(2, 2), Piece(PieceType.Pawn, Colour.BLACK))
        # Create game
        self.game = Game(self.board, Colour.WHITE, [Move(Position(3, 6), Position(3, 4))])

    def test_is_check(self):
        """Test of is_check() method.
        """

        assert not GameLogic.is_check(self.game.board, self.game.turn)

    def test_make_move(self):
        """Test of make_move() method.
        """

        # Check short castling
        game = GameLogic.make_move(Move(Position(4, 0), Position(6, 0)), self.game)
        assert game.turn != self.game.turn
        assert game.history_moves[-1] == Move(Position(4, 0), Position(6, 0))
        assert game.board.get_piece(Position(4, 0)) is None
        assert game.board.get_piece(Position(5, 0)).type == PieceType.Rook
        assert game.board.get_piece(Position(6, 0)).type == PieceType.King
        assert game.board.get_piece(Position(7, 0)) is None
        # Check long castling
        game = GameLogic.make_move(Move(Position(4, 0), Position(2, 0)), self.game)
        assert game.turn != self.game.turn
        assert game.history_moves[-1] == Move(Position(4, 0), Position(2, 0))
        assert game.board.get_piece(Position(4, 0)) is None
        assert game.board.get_piece(Position(3, 0)).type == PieceType.Rook
        assert game.board.get_piece(Position(2, 0)).type == PieceType.King
        assert game.board.get_piece(Position(1, 0)) is None
        assert game.board.get_piece(Position(0, 0)) is None
        # Check en_passant
        game = GameLogic.make_move(Move(Position(4, 4), Position(3, 5)), self.game)
        assert game.turn != self.game.turn
        assert game.history_moves[-1] == Move(Position(4, 4), Position(3, 5))
        assert game.board.get_piece(Position(4, 4)) is None
        assert game.board.get_piece(Position(3, 5)).type == PieceType.Pawn
        assert game.board.get_piece(Position(3, 5)).colour == Colour.WHITE
        assert game.board.get_piece(Position(3, 4)) is None

    def test_is_move_possible(self):
        """Test of is_move_possible() method.
        """

        assert not GameLogic.is_move_possible(self.game, Move(Position(4, 1), Position(3, 2)))
        assert not GameLogic.is_move_possible(self.game, Move(Position(4, 0), Position(3, 1)))
        assert not GameLogic.is_move_possible(self.game, Move(Position(4, 0), Position(4, -1)))
        assert not GameLogic.is_move_possible(self.game, Move(Position(2, 2), Position(2, 1)))
        assert GameLogic.is_move_possible(self.game, Move(Position(4, 0), Position(5, 1)))
        assert GameLogic.is_move_possible(self.game, Move(Position(4, 0), Position(2, 0)))
        assert GameLogic.is_move_possible(self.game, Move(Position(4, 0), Position(6, 0)))
