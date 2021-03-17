#!/usr/bin/python3

from enum import Enum
from typing import List

from entities.colour import Colour


class Castle(Enum):
    WHITE_SHORT = 0
    WHITE_LONG = 1
    BLACK_SHORT = 2
    BLACK_LONG = 3


class PossibleCastle(object):

    def __init__(self,
                 white_short: bool = True,
                 white_long: bool = True,
                 black_short: bool = True,
                 black_long: bool = True):
        self.list_castles = []
        if white_short:
            self.list_castles.append(Castle.WHITE_SHORT)
        if white_long:
            self.list_castles.append(Castle.WHITE_LONG)
        if black_short:
            self.list_castles.append(Castle.BLACK_SHORT)
        if black_long:
            self.list_castles.append(Castle.BLACK_LONG)

    def get_castle_from_colour(self, colour: Colour) -> List[bool]:
        """Returns if short and long castles are possible.
        """
        if colour == Colour.WHITE:
            return Castle.WHITE_SHORT in self.list_castles, \
                   Castle.WHITE_LONG in self.list_castles
        else:
            return Castle.BLACK_SHORT in self.list_castles, \
                   Castle.BLACK_LONG in self.list_castles

