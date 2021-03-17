from typing import Union, List

from engine.game import Game
from entities.board import Board
from entities.pieces import Pieces
from entities.position import Position
from entities.colour import Colour
from entities.possible_castle import PossibleCastle, Castle
from engine.utils import change_val_and_key


class FEN(object):
    """Class used to serialize to or deserialize from FEN notation.

    https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    """

    piece_to_str = {
        Pieces.WHITE_KING: 'K',
        Pieces.WHITE_QUEEN: 'Q',
        Pieces.WHITE_BISHOP: 'R',
        Pieces.WHITE_KNIGHT: 'B',
        Pieces.WHITE_ROOK: 'N',
        Pieces.WHITE_PAWN: 'P',

        Pieces.BLACK_KING: 'k',
        Pieces.BLACK_QUEEN: 'q',
        Pieces.BLACK_BISHOP: 'r',
        Pieces.BLACK_KNIGHT: 'b',
        Pieces.BLACK_ROOK: 'n',
        Pieces.BLACK_PAWN: 'p'
    }
    str_to_piece = change_val_and_key(piece_to_str)

    colour_to_str = {
        Colour.WHITE: 'w',
        Colour.BLACK: 'b'
    }
    str_to_colour = change_val_and_key(colour_to_str)

    castle_to_str = {
        Castle.WHITE_LONG: 'Q',
        Castle.WHITE_SHORT: 'K',
        Castle.BLACK_LONG: 'q',
        Castle.BLACK_SHORT: 'k'
    }
    str_to_castle = change_val_and_key(castle_to_str)

    x_to_str = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h'
    }
    str_to_x = change_val_and_key(x_to_str)

    @staticmethod
    def board_to_fen(board: Board, sep: str = '/') -> str:
        """Converts board into FEN notation.
        """

        fen_not = []
        for y in range(7, -1, -1):
            row = []
            missing_in_row = 0
            for x in range(0, 8):
                pos = Position(x, y)
                if board.is_position_empty(pos):
                    missing_in_row += 1
                    if missing_in_row > 1:
                        row[-1] = str(missing_in_row)
                    else:
                        row.append(str(missing_in_row))
                else:
                    missing_in_row = 0
                    row.append(FEN.piece_to_str[board.get_piece(pos)])
            fen_not.append(''.join(row))
        return sep.join(fen_not)

    @staticmethod
    def fen_to_board(fen_not: str) -> Board:
        """Converts FEN notation into board.
        """

        board = Board()
        rows = fen_not.split('/')  # from 7th to 0th
        for y, row in enumerate(rows[::-1]):
            x = 0
            for character in row:
                if character.isdigit():
                    x += int(character)
                else:
                    pos, piece = Position(x, y), FEN.str_to_piece[character]
                    board.set_piece(pos, piece)
                    x += 1
        return board

    @staticmethod
    def colour_to_fen(colour: Colour) -> str:
        assert colour in FEN.colour_to_str.keys(), 'Invalid colour'
        return FEN.colour_to_str[colour]

    @staticmethod
    def fen_to_colour(fen_not: str) -> Colour:
        assert fen_not in FEN.str_to_colour.keys(), f'Invalid colour {fen_not}'
        return FEN.str_to_colour[fen_not]

    @staticmethod
    def castle_to_fen(possible_castle: PossibleCastle, empt_symb: str = '-') -> str:
        fen_not = ''.join([FEN.castle_to_str[castle] for castle in possible_castle.list_castles])
        if fen_not == '':
            fen_not = empt_symb
        return fen_not

    @staticmethod
    def fen_to_castle(fen_not: str, empt_symb: str = '-') -> PossibleCastle:
        possible_castle = PossibleCastle()
        if fen_not != empt_symb:
            possible_castle.list_castles = [FEN.str_to_castle[character] for character in fen_not]
            return possible_castle
        else:
            possible_castle.list_castles = []
            return possible_castle

    @staticmethod
    def fen_to_pos(fen_not: str, empt_symb: str = '-'):
        if fen_not == empt_symb:
            return
        else:
            x, y = FEN.str_to_x[fen_not[0]], int(fen_not[1]) - 1
            return Position(x, y)

    @staticmethod
    def pos_to_fen(pos: Union[None, Position], empt_symb: str = '-') -> str:
        if pos is None:
            return empt_symb
        else:
            return f'{FEN.x_to_str[pos.x]}{pos.y+1}'

    @staticmethod
    def fen_to_game(fen_not: str) -> Game:
        board_fen, turn_fen, possible_castle_fen, en_passant_fen = FEN.split_fen_not(fen_not)
        board = FEN.fen_to_board(board_fen)
        turn = FEN.fen_to_colour(turn_fen)
        possible_castle = FEN.fen_to_castle(possible_castle_fen)
        en_passant_fen = FEN.fen_to_pos(en_passant_fen)
        return Game(board, turn, possible_castle, en_passant_fen)

    @staticmethod
    def game_to_fen(game: Game) -> str:
        board_fen = FEN.board_to_fen(game.board)
        turn_fen = FEN.colour_to_fen(game.turn)
        possible_castle_fen = FEN.castle_to_fen(game.castle)
        en_passant_fen = FEN.pos_to_fen(game.en_passant)
        fen_not = FEN.join_fen_not(board_fen, turn_fen, possible_castle_fen, en_passant_fen)
        return fen_not

    @staticmethod
    def split_fen_not(fen_not) -> List[str]:
        fen_not_split = fen_not.split(' ')
        assert len(fen_not_split) == 4
        board_fen, turn_fen, possible_castle_fen, en_passant_fen = fen_not_split
        return board_fen, turn_fen, possible_castle_fen, en_passant_fen

    @staticmethod
    def join_fen_not(board_fen: str, turn_fen: str, possible_castle_fen: str, en_passant_fen: str) -> str:
        return ' '.join([board_fen, turn_fen, possible_castle_fen, en_passant_fen])


if __name__ == "__main__":

    from entities.move import Move
    from engine.logic import GameLogic

    game1 = Game.create_start_game()
    print(FEN.game_to_fen(game1))

    move = Move(Position(4, 1), Position(4, 3))
    game2 = GameLogic.make_move(move, game1)
    print(FEN.game_to_fen(game2))

    move = Move(Position(4, 6), Position(4, 4))
    game3 = GameLogic.make_move(move, game2)
    print(FEN.game_to_fen(game3))

    move = Move(Position(4, 0), Position(4, 1))
    game4 = GameLogic.make_move(move, game3)
    print(FEN.game_to_fen(game4))

    move = Move(Position(4, 0), Position(4, 1))
    game5 = GameLogic.make_move(move, game4)
    print(FEN.game_to_fen(game5))
