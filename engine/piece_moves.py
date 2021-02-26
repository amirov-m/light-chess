#!/usr/bin/python3

from __future__ import annotations

from typing import List

from engine.game import Game
from engine.positions_under_threat import PositionsUnderThreat
from entities.colour import Colour
from entities.move import Move
from entities.pieces import PieceType
from entities.position import Position


class PieceMoves:
    """Class used to make move. This class is technically PositionsUnderThreat with taking into
    account en_passant and castling.

    ATTENTION: not taking into account check after moves, doing it ONLY for castling!!!
    """

    @staticmethod
    def moves(piece_type: PieceType, position: Position, game: Game) -> List[Move]:
        """Return list of possible moves by piece from <game.turn> side."""

        # Retrieve piece.
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
        """Return all moves of <game.turn> turn."""

        moves = []
        for pos in game.board.get_positions_for_side(game.turn):
            moves.extend(PieceMoves.moves(game.board.get_piece(pos).type, pos, game))
        return moves

    @staticmethod
    def is_piece_touched(pos: Position, game: Game):
        """Check if piece is being touched. Check if there are at least one occurrence of move/touch
        in history."""

        # Check if positions are being touched at least once.
        return any(pos in [move.start, move.finish] for move in game.history_moves)

    @staticmethod
    def en_passant_moves(pos: Position, game: Game) -> List[Move]:
        """Return list of <game.turn> en passant moves.
        en passant:
            - opponent pawn makes the move at previous turn
            - opponent pawn jumps over 2 positions
        """

        # Init list of moves.
        en_passant = []
        if len(game.history_moves) != 0:
            # Retrieve start piece.
            piece_start = game.board.get_piece(pos)
            # Check if piece_start not empty.
            if piece_start is not None and piece_start.type == PieceType.PAWN:
                # 2 directions.
                shifts = [(-1, 0), (1, 0)]
                for shift_x, shift_y in shifts:
                    # Retrieve not start piece.
                    piece = game.board.get_piece(Position(pos.x + shift_x, pos.y + shift_y))
                    if piece is not None and piece.type == PieceType.PAWN:
                        # Retrieve last_move.
                        last_move = game.history_moves[-1]
                        # Check if pawn makes the last move and if it jumps over 2 positions.
                        if (
                            Position(pos.x + shift_x, pos.y + shift_y) == last_move.finish
                            and abs(last_move.start.y - last_move.finish.y) == 2
                        ):
                            # Add move in dependence of colour.
                            if game.turn == Colour.WHITE:
                                move = Move(pos, Position(pos.x + shift_x, pos.y + 1))
                                en_passant.append(move)
                            else:
                                move = Move(pos, Position(pos.x + shift_x, pos.y - 1))
                                en_passant.append(move)
        return en_passant

    @staticmethod
    def castling_moves(pos: Position, game: Game) -> List[Move]:
        """Return list of <game.turn> castling moves.
        Check is taking into account!!!
        """

        # Init catling list.
        castling = []
        # Retrieve piece at start position.
        piece_start = game.board.get_piece(pos)
        # Retrieve positions under threat (important info for castling).
        pos_under_threat = PositionsUnderThreat.all_positions_under_threat_for_side(
            game.turn, game.board
        )
        # Check if piece piece at start position King with no threat/check.
        if (
            piece_start is not None
            and piece_start.type == PieceType.KING
            and not PieceMoves.is_piece_touched(pos, game)
            and pos not in pos_under_threat
        ):
            # Short castling. _1r_ means 1 pos to the right from white side.
            is_1r_pos_avail = (
                game.board.is_position_empty(Position(pos.x + 1, pos.y))
                and Position(pos.x + 1, pos.y) not in pos_under_threat
            )
            is_2r_pos_avail = (
                game.board.is_position_empty(Position(pos.x + 2, pos.y))
                and Position(pos.x + 2, pos.y) not in pos_under_threat
            )
            is_3r_pos_rook = (
                not game.board.is_position_empty(Position(pos.x + 3, pos.y))
                and game.board.get_piece(Position(pos.x + 3, pos.y)).type
                == PieceType.ROOK
            )
            if (
                is_1r_pos_avail
                and is_2r_pos_avail
                and is_3r_pos_rook
                and not PieceMoves.is_piece_touched(Position(pos.x + 3, pos.y), game)
            ):
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
            is_4l_pos_rook = (
                not game.board.is_position_empty(Position(pos.x - 4, pos.y))
                and game.board.get_piece(Position(pos.x - 4, pos.y)).type
                == PieceType.ROOK
            )
            if (
                is_1l_pos_avail
                and is_2l_pos_avail
                and is_4l_pos_rook
                and game.board.is_position_empty(Position(pos.x - 3, pos.y))
                and not PieceMoves.is_piece_touched(Position(pos.x - 4, pos.y), game)
            ):
                move = Move(pos, Position(pos.x - 2, pos.y))
                castling.append(move)
        return castling

    @staticmethod
    def pawn_moves(pos: Position, game: Game) -> List[Move]:
        """Return list of <game.turn> pawn moves.
        pawn moves = positions_under_threat + move forward + en_passant
        """

        # Init move list
        moves = []
        # Check if position under threat occupied with opponent pieces or en_passant possible.
        for pos_under_threat in PositionsUnderThreat.positions_under_pawn_threat(
            pos, game.turn, game.board
        ):
            move = Move(pos, pos_under_threat)
            if PositionsUnderThreat.is_position_enemy(
                pos_under_threat, game.turn, game.board
            ) or move in PieceMoves.en_passant_moves(pos, game):
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
        if (
            game.board.is_position_empty(pos_forward)
            and game.board.is_position_empty(pos_d_forward)
            and not PieceMoves.is_piece_touched(pos, game)
        ):
            move = Move(pos, pos_d_forward)
            moves.append(move)
        return moves

    @staticmethod
    def rook_moves(pos: Position, game: Game) -> List[Move]:
        """Return list of <game.turn> rook moves.
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
        """Return list of <game.turn> knight moves.
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
        """Return list of <game.turn> bishop moves.
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
        """Return list of <game.turn> queen moves.
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
        """Return list of <game.turn> king moves.
        king moves = positions_under_threat + castling
        """

        moves = [
            Move(pos, pos_threat)
            for pos_threat in PositionsUnderThreat.positions_under_king_threat(
                pos, game.turn, game.board
            )
        ]
        return [*PieceMoves.castling_moves(pos, game), *moves]
