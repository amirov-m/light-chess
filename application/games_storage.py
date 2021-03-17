from engine.game import Game
from engine.fen import FEN
from application.db_tables.game_table import GameTable


class GamesStorage(object):
    def create_new_game(self):
        game = Game.create_start_game()
        fen_not = FEN.game_to_fen(game)
        board_fen, turn_fen, possible_castle_fen, en_passant_fen = FEN.split_fen_not(fen_not)
        row = GameTable.add_row(board_fen, turn_fen, possible_castle_fen, en_passant_fen)
        return row.game_id, game

    def get_by_id(self, game_id: int):
        row = GameTable.get_row_by_game_id(game_id)
        return row

    def write(self, game_id: int, piece_placement: str, active_colour: str,
              castling_availability: str, en_passant: str):
        GameTable.update_row_by_game_id(game_id, piece_placement, active_colour, castling_availability, en_passant)


games_storage_singleton = GamesStorage()
