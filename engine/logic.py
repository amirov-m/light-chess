#!/usr/bin/python3

from __future__ import annotations

import copy

from engine.game import Game
from engine.piece_moves import PieceMoves
from engine.positions_under_threat import PositionsUnderThreat
from entities.board import Board
from entities.colour import Colour
from entities.move import Move
from entities.pieces import Piece, PieceType
from entities.position import Position
from engine.piece_moves import PieceMoves


class GameLogic:
    """Class used to handle game logic. This class is technically utilization of PieceMoves with
    additional checking of check after each move. 3 main method: is_mate(), is_check() and
    make_move() are necessary to handle chess game.
    """

    @staticmethod
    def is_mate(game: Game):
        """Check if <game.turn> side got mate.
        mate = check without possibility to defend own king
        """

        if GameLogic.is_check(game.board, game.turn):
            for move in PieceMoves.all_moves(game):
                if GameLogic.is_move_possible(game, move):
                    return False
            return True
        return False

    @staticmethod
    def is_check(board: Board, colour: Colour) -> bool:
        """Check if <colour> side got check.
        check = at least one opponent piece aims at own king
        """

        # Retrieve king position
        king_pos = board.get_positions_for_piece(Piece(PieceType.KING, colour))[0]
        return king_pos in PositionsUnderThreat.all_positions_under_threat_for_side(
            colour, board
        )

    @staticmethod
    def make_move(move: Move, game: Game) -> Game:
        """Make move.

        Attention: no checking of check after move. Technically move can be not valid!!!
        """

        # Copy game (pass by value)
        game = copy.deepcopy(game)
        # Retrieve piece at start position
        piece = game.board.get_piece(move.start)
        # Get possible moves
        possible_moves = PieceMoves.moves(piece.type, move.start, game)
        # Check if move satisfies
        if move in possible_moves:
            # Check if castling occurs
            if move in PieceMoves.castling_moves(move.start, game):
                game.board.set_piece(
                    Position(int((move.finish.x + move.start.x) / 2), move.start.y),
                    Piece(PieceType.ROOK, game.turn),
                )
                # Short castling
                if move.finish.x - move.start.x > 0:
                    game.board.remove_piece(Position(7, move.start.y))
                # Long castling
                else:
                    game.board.remove_piece(Position(0, move.start.y))
            # Check if en passant occurs
            if move in PieceMoves.en_passant_moves(move.start, game):
                game.board.remove_piece(Position(move.finish.x, move.start.y))
            # Update board
            game.board.set_piece(move.finish, piece)
            game.board.remove_piece(move.start)
            # Update history
            game.history_moves.append(move)
        return Game(game.board, Colour.change_colour(game.turn), game.history_moves)

    @staticmethod
    def is_move_possible(game: Game, move: Move) -> bool:
        """Check if move possible."""

        # Get piece at start position
        piece = game.board.get_piece(move.start)
        # Check if figure exists.
        if piece is None:
            return False
        # Check if colours match.
        if game.turn != piece.colour:
            return False
        # Check if x and y vary between 0 (included) and 7 (included)
        if not Board.is_position_on_board(move.finish, game.board):
            return False
        # Make move
        further_game = GameLogic.make_move(move, game)
        if len(further_game.history_moves) == len(game.history_moves):
            return False
        # Check if check occurs after making move
        return not GameLogic.is_check(
            further_game.board, Colour.change_colour(further_game.turn)
        )
