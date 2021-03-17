from typing import Dict
from application.games_storage import games_storage_singleton
from flask_restful import Resource, reqparse

from engine.fen import FEN
from engine.logic import GameLogic
from entities.move import Move


class MakeMove(Resource):
    put_args = reqparse.RequestParser()
    put_args.add_argument("game_id", type=int, required=True)
    put_args.add_argument("start_pos", required=True)
    put_args.add_argument("end_pos", required=True)

    def post(self) -> Dict[str, str]:
        args = self.put_args.parse_args()
        row = games_storage_singleton.get_by_id(args["game_id"])
        fen_not = FEN.join_fen_not(row.piece_placement, row.active_colour,
                                   row.castling_availability, row.en_passant)
        game = FEN.fen_to_game(fen_not)
        start_pos = FEN.fen_to_pos(args["start_pos"])
        end_pos = FEN.fen_to_pos(args["end_pos"])
        move = Move(start_pos, end_pos)
        if GameLogic.is_move_possible(game, move):
            status = "OK"
            next_game = GameLogic.make_move(move, game)
            next_fen_not = FEN.game_to_fen(next_game)
            piece_placement, active_colour, castling_availability, en_passant = FEN.split_fen_not(next_fen_not)
            games_storage_singleton.write(args["game_id"], piece_placement, active_colour, castling_availability,
                                          en_passant)
        else:
            status = "WrongMove"
        return {"Status": status}
