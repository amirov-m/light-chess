#!/usr/bin/python3

from __future__ import annotations

import itertools
from typing import List

from entities.board import Board
from entities.colour import Colour
from entities.pieces import Piece, PieceType
from entities.position import Position


class PositionsUnderThreat:
    """Class used to to return list of positions under thread. 'under thread' means all positions
    which enemy king cannot reach, because of the check.
    """

    @staticmethod
    def is_position_enemy(pos: Position, colour: Colour, board: Board) -> bool:
        """Checks if position occupied with enemy piece."""

        # Retrieve piece.
        piece = board.get_piece(pos)
        return piece is not None and piece.colour != colour

    @staticmethod
    def is_position_enemy_or_empty(pos: Position, colour: Colour, board: Board) -> bool:
        """Checks if position occupied with enemy piece or empty.
        Returns False if pos is out of the board.
        """

        # Check if pos locates on the board.
        return Board.is_position_on_board(pos, board) and (
            PositionsUnderThreat.is_position_enemy(pos, colour, board)
            or board.is_position_empty(pos)
        )

    @staticmethod
    def check_positions(
        pos: Position, colour: Colour, board: Board, shifts: list
    ) -> List[Position]:
        """Checks which positions are possible."""

        # Init position list.
        positions_under_threat = []
        # Iterate through shifts.
        for shift_x, shift_y in shifts:
            # Check if shift is possible, otherwise break the loop.
            if PositionsUnderThreat.is_position_enemy_or_empty(
                Position(pos.x + shift_x, pos.y + shift_y), colour, board
            ):
                # Add shift
                positions_under_threat.append(
                    Position(pos.x + shift_x, pos.y + shift_y)
                )
        return positions_under_threat

    @staticmethod
    def check_positions_with_obstacles(
        pos: Position, colour: Colour, board: Board, shifts: list
    ) -> List[Position]:
        """Checks which positions are possible.

        Iterates through shifts till the first obstacle. Obstacle means own or enemy piece.
        """

        # Init position list.
        positions_under_threat = []
        # Iterates though shifts.
        for shift_x, shift_y in shifts:
            # Check if shift is possible, otherwise break the loop.
            if not PositionsUnderThreat.is_position_enemy_or_empty(
                Position(pos.x + shift_x, pos.y + shift_y), colour, board
            ):
                break
            # Add shift
            positions_under_threat.append(Position(pos.x + shift_x, pos.y + shift_y))
            # Check if position is occupied with enemy piece, otherwise break the loop.
            if PositionsUnderThreat.is_position_enemy(
                Position(pos.x + shift_x, pos.y + shift_y), colour, board
            ):
                break
        return positions_under_threat

    @staticmethod
    def all_positions_under_threat_for_side(
        colour: Colour, board: Board
    ) -> List[Position]:
        positions_under_threat = []
        for pos in board.get_positions_for_side(Colour.change_colour(colour)):
            positions_under_threat.extend(
                PositionsUnderThreat.positions_under_threat(
                    pos, board.get_piece(pos), board
                )
            )
        return positions_under_threat

    @staticmethod
    def positions_under_threat(
        pos: Position, piece: Piece, board: Board
    ) -> List[Position]:

        pos_types = {
            PieceType.KING: PositionsUnderThreat.positions_under_king_threat,
            PieceType.QUEEN: PositionsUnderThreat.positions_under_queen_threat,
            PieceType.BISHOP: PositionsUnderThreat.positions_under_bishop_threat,
            PieceType.KNIGHT: PositionsUnderThreat.positions_under_knight_threat,
            PieceType.ROOK: PositionsUnderThreat.positions_under_rook_threat,
            PieceType.PAWN: PositionsUnderThreat.positions_under_pawn_threat,
        }

        return pos_types[piece.type](pos, piece.colour, board)

    @staticmethod
    def positions_under_king_threat(
        pos: Position, colour: Colour, board: Board
    ) -> List[Position]:
        """Returns list of positions under threat by king."""

        # Init list of shifts
        shifts = list(itertools.product([-1, 0, 1], repeat=2))
        return PositionsUnderThreat.check_positions(pos, colour, board, shifts)

    @staticmethod
    def positions_under_queen_threat(
        position: Position, colour: Colour, board: Board
    ) -> List[Position]:
        """Returns list of positions under threat by queen.

        Can be calculated by combining returns from bishop and rook methods.
        """

        return [
            *PositionsUnderThreat.positions_under_rook_threat(position, colour, board),
            *PositionsUnderThreat.positions_under_bishop_threat(
                position, colour, board
            ),
        ]

    @staticmethod
    def positions_under_bishop_threat(
        pos: Position, colour: Colour, board: Board
    ) -> List[Position]:
        """Returns list of positions under threat by bishop.

        Checks 4 directions till the first obstacle: up_right, down_right, down_left and up_left.
        """

        # Init lists of shifts.
        shifts_up_right = [(shift, shift) for shift in range(1, board.height)]
        shifts_down_right = [(shift, -shift) for shift in range(1, board.height)]
        shifts_down_left = [(-shift, -shift) for shift in range(1, board.height)]
        shifts_up_left = [(-shift, shift) for shift in range(1, board.height)]
        # Init position list.
        positions_under_threat = []
        # Iterate over 4 directions.
        for shifts in [
            shifts_up_right,
            shifts_down_right,
            shifts_down_left,
            shifts_up_left,
        ]:
            positions_under_threat = [
                *positions_under_threat,
                *PositionsUnderThreat.check_positions_with_obstacles(
                    pos, colour, board, shifts
                ),
            ]
        return positions_under_threat

    @staticmethod
    def positions_under_knight_threat(
        pos: Position, colour: Colour, board: Board
    ) -> List[Position]:
        """Returns list of positions under threat by knight."""

        # Init list of shifts.
        shifts = [
            *list(itertools.product([-1, 1], [-2, 2])),
            *list(itertools.product([-2, 2], [-1, 1])),
        ]
        return PositionsUnderThreat.check_positions(pos, colour, board, shifts)

    @staticmethod
    def positions_under_rook_threat(
        pos: Position, colour: Colour, board: Board
    ) -> List[Position]:
        """Returns list of positions under threat by rook.

        Checks 4 directions till the first obstacle: up, right, down and left.
        """

        # Init lists of shifts.
        shifts_up = [(0, shift_y) for shift_y in range(1, board.height)]
        shifts_right = [(shift_x, 0) for shift_x in range(1, board.width)]
        shifts_down = [(0, shift_y) for shift_y in range(-1, -board.height, -1)]
        shifts_left = [(shift_x, 0) for shift_x in range(-1, -board.width, -1)]
        # Init position list.
        positions_under_threat = []
        # Iterate over directions
        for shifts in [shifts_up, shifts_right, shifts_down, shifts_left]:
            positions_under_threat = [
                *positions_under_threat,
                *PositionsUnderThreat.check_positions_with_obstacles(
                    pos, colour, board, shifts
                ),
            ]
        return positions_under_threat

    @staticmethod
    def positions_under_pawn_threat(
        pos: Position, colour: Colour, board: Board
    ) -> List[Position]:
        """Returns list of positions under threat by pawn."""

        # Init list of shifts.
        if colour == Colour.WHITE:
            shifts = [(-1, 1), (1, 1)]
        else:
            shifts = [(-1, -1), (1, -1)]
        return PositionsUnderThreat.check_positions(pos, colour, board, shifts)
