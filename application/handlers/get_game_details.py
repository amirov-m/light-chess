from typing import Dict
from application.games_storage import games_storage_singleton
from flask_restful import Resource, reqparse

from engine.fen import FEN


class GetGameDetails(Resource):
    put_args = reqparse.RequestParser()
    put_args.add_argument("game_id", type=int, required=True)

    def get(self) -> Dict[str, str]:
        args = self.put_args.parse_args()
        row = games_storage_singleton.get_by_id(args["game_id"])
        fen_not = FEN.join_fen_not(row.piece_placement, row.active_colour,
                                   row.castling_availability, row.en_passant)
        return {"FEN": fen_not}
