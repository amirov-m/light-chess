#!/usr/bin/python3

from __future__ import annotations

from typing import NamedTuple, Union

from entities.board import Board
from entities.colour import Colour
from entities.possible_castle import PossibleCastle
from entities.move import Position


class Game(NamedTuple):
    board: Board
    turn: Colour
    castle: PossibleCastle
    en_passant: Union[None, Position] = None

    @staticmethod
    def create_start_game() -> Game:
        start_board = Board.create_start_board()
        castle = PossibleCastle()
        return Game(start_board, Colour.WHITE, castle)
