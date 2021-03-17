#!/usr/bin/python3

from __future__ import annotations

from typing import List

from engine.game import Game
from engine.positions_under_threat import PositionsUnderThreat
from entities.colour import Colour
from entities.move import Move
from entities.pieces import PieceType
from entities.position import Position
from entities.possible_castle import PossibleCastle


class PieceMoves:
    """Class used to make move. This class is technically PositionsUnderThreat with taking into
    account en_passant and castling.

    ATTENTION: not taking into account check after moves, doing it ONLY for castling!!!
    """

    @staticmethod
    def moves(piece_type: PieceType, position: Position, game: Game) -> List[Move]:
        """Returns list of possible moves by piece from <game.turn> side."""

        piece = game.board.get_piece(position)

        piece_types = {
            piece_type.KING: PieceMoves.king_moves,
            piece_type.QUEEN: PieceMoves.queen_moves,
            piece_type.BISHOP: PieceMoves.bishop_moves,
            piece_type.KNIGHT: PieceMoves.knight_moves,
            piece_type.ROOK: PieceMoves.rook_moves,
            piece_type.PAWN: PieceMoves.pawn_moves,
        }

        assert piece.type in piece_types.keys()
        return piece_types[piece.type](position, game)

    @staticmethod
    def all_moves(game: Game) -> List[Move]:
        """Returns all moves of <game.turn> turn."""

        moves = []
        for pos in game.board.get_positions_for_side(game.turn):
            moves.extend(PieceMoves.moves(game.board.get_piece(pos).type, pos, game))
        return moves

    @staticmethod
    def castling_moves(pos: Position, game: Game) -> List[Move]:
        """Returns list of <game.turn> castling moves.
        Check is taking into account!!!
        """

        castling = []
        piece_start = game.board.get_piece(pos)

        pos_under_threat = PositionsUnderThreat.all_positions_under_threat_for_side(
            game.turn, game.board
        )
        is_short_castling, is_long_castling = game.castle.get_castle_from_colour(game.turn)
        if (
            piece_start is not None
            and piece_start.type == PieceType.KING
            and pos not in pos_under_threat
        ):
            # Short castling. _1r_ means 1 pos to the right from white side/view.
            is_1r_pos_avail = (
                game.board.is_position_empty(Position(pos.x + 1, pos.y))
                and Position(pos.x + 1, pos.y) not in pos_under_threat
            )
            is_2r_pos_avail = (
                game.board.is_position_empty(Position(pos.x + 2, pos.y))
                and Position(pos.x + 2, pos.y) not in pos_under_threat
            )
            if is_short_castling and is_1r_pos_avail and is_2r_pos_avail:
                move = Move(pos, Position(pos.x + 2, pos.y))
                castling.append(move)

            # Long castling. _1l_ means 1 pos to the left from white side.
            is_1l_pos_avail = (
                game.board.is_position_empty(Position(pos.x - 1, pos.y))
                and Position(pos.x - 1, pos.y) not in pos_under_threat
            )
            is_2l_pos_avail = (
                game.board.is_position_empty(Position(pos.x - 2, pos.y))
                and Position(pos.x - 2, pos.y) not in pos_under_threat
            )
            is_3l_pos_avail = game.board.is_position_empty(Position(pos.x - 2, pos.y))

            if (
                is_long_castling
                and is_1l_pos_avail
                and is_2l_pos_avail
                and is_3l_pos_avail
            ):
                move = Move(pos, Position(pos.x - 2, pos.y))
                castling.append(move)
        return castling

    @staticmethod
    def pawn_moves(pos: Position, game: Game) -> List[Move]:
        """Returns list of <game.turn> pawn moves.

        pawn moves = positions_under_threat with enemy pieces + move forward + en_passant
        """

        moves = []

        # Check chop down
        for pos_under_threat in PositionsUnderThreat.positions_under_pawn_threat(
            pos, game.turn, game.board
        ):
            move = Move(pos, pos_under_threat)
            if PositionsUnderThreat.is_position_enemy(
                pos_under_threat, game.turn, game.board
            ) or move.finish == game.en_passant:
                moves.append(move)

        # Check forward move.
        shift_forward_y = 1 if game.turn == Colour.WHITE else -1
        pos_forward = Position(pos.x, pos.y + shift_forward_y)
        if game.board.is_position_empty(pos_forward):
            move = Move(pos, pos_forward)
            moves.append(move)

        # Check double move forward
        shift_forward_y = 2 if game.turn == Colour.WHITE else -2
        pos_d_forward = Position(pos.x, pos.y + shift_forward_y)
        is_not_touched = pos.y == 1 if game.turn == Colour.WHITE else pos.y == 6
        if (
            game.board.is_position_empty(pos_forward)
            and game.board.is_position_empty(pos_d_forward)
            and is_not_touched
        ):
            move = Move(pos, pos_d_forward)
            moves.append(move)
        return moves

    @staticmethod
    def rook_moves(pos: Position, game: Game) -> List[Move]:
        """Returns list of <game.turn> rook moves.

        rook moves = positions_under_threat
        """

        moves = [
            Move(pos, pos_threat)
            for pos_threat in PositionsUnderThreat.positions_under_rook_threat(
                pos, game.turn, game.board
            )
        ]
        return moves

    @staticmethod
    def knight_moves(pos: Position, game: Game) -> List[Move]:
        """Returns list of <game.turn> knight moves.

        knight moves = positions_under_threat
        """

        moves = [
            Move(pos, pos_threat)
            for pos_threat in PositionsUnderThreat.positions_under_knight_threat(
                pos, game.turn, game.board
            )
        ]
        return moves

    @staticmethod
    def bishop_moves(pos: Position, game: Game) -> List[Position]:
        """Returns list of <game.turn> bishop moves.

        bishop moves = positions_under_threat
        """

        moves = [
            Move(pos, pos_threat)
            for pos_threat in PositionsUnderThreat.positions_under_bishop_threat(
                pos, game.turn, game.board
            )
        ]
        return moves

    @staticmethod
    def queen_moves(pos: Position, game: Game) -> List[Position]:
        """Returns list of <game.turn> queen moves.

        queen moves = positions_under_threat
        """

        moves = [
            Move(pos, pos_threat)
            for pos_threat in PositionsUnderThreat.positions_under_queen_threat(
                pos, game.turn, game.board
            )
        ]
        return moves

    @staticmethod
    def king_moves(pos: Position, game: Game) -> List[Position]:
        """Returns list of <game.turn> king moves.

        king moves = positions_under_threat + castling
        """

        moves = [
            Move(pos, pos_threat)
            for pos_threat in PositionsUnderThreat.positions_under_king_threat(
                pos, game.turn, game.board
            )
        ]
        return [*PieceMoves.castling_moves(pos, game), *moves]
