import pickle
import json
import base64
from typing import Tuple, Dict
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from engine.game import Game
from engine.logic import GameLogic
from entities.move import Move
from entities.position import Position
from engine.piece_moves import PieceMoves


app = Flask(__name__)
api = Api(app)
app.config['SQLaCHEMY_DATAbASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class DB(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.LargeBinary)


db.create_all()


def obj_to_bytes(obj):
    return pickle.dumps(obj)

def obj_to_json(obj):
    return base64.b64encode(obj_to_bytes(obj)).decode('utf-8')

def json_to_obj(json_bytes):
    return bytes_to_obj(base64.b64decode(json_bytes))

def bytes_to_obj(bytes):
    return pickle.loads(bytes)


class CreatGame(Resource):
    resource_fields = {
        'game_id': fields.Integer
    }

    @marshal_with(resource_fields)
    def get(self) -> Dict[str, int]:
        game_id = self.gen_id()
        game = Game.create_start_game()
        game_bytes = obj_to_bytes(game)

        row = DB(game_id=game_id, game=game_bytes)
        db.session.add(row)
        db.session.commit()
        return row

    @staticmethod
    def gen_id() -> Tuple[int, int]:
        """Returns incremented game_id and gui_id equals to 0
        """
        max_game_id = db.session.query(func.max(DB.game_id)).scalar()
        max_game_id = max_game_id if max_game_id is not None else -1
        return max_game_id+1


class GetPossibleMoves(Resource):
    put_args = reqparse.RequestParser()
    put_args.add_argument("game_id", type=int, required=True)

    def get(self):
        args = self.put_args.parse_args()
        row = DB.query.filter_by(game_id=args['game_id']).first()
        if not row:
            print("Here")
            abort(404, message=f"{args['game_id']} not found")
        game = bytes_to_obj(row.game)
        moves = PieceMoves.all_moves(game)
        return {'possibleMoves': obj_to_json(moves)}


class MakeMove(Resource):
    put_args = reqparse.RequestParser()
    put_args.add_argument("game_id", type=int, required=True)
    put_args.add_argument("move", required=True)

    def post(self) -> Dict[str, str]:
        args = self.put_args.parse_args()
        row = DB.query.filter_by(game_id=args['game_id']).first()
        if not row:
            abort(404, message=f"{args['game_id']} not found")
        move = json_to_obj(args['move'])
        game = bytes_to_obj(row.game)
        if GameLogic.is_move_possible(game, move):
            next_game = GameLogic.make_move(move, game)
            row.game = obj_to_bytes(next_game)
            db.session.commit()
            status = "Ok"
        else:
            status = "WrongMove"
        return {'status': status}

api.add_resource(CreatGame, "/createGame/")
api.add_resource(MakeMove, "/makeMove/")
api.add_resource(GetPossibleMoves, "/getPossibleMoves/")


if __name__ == "__main__":
    app.run(debug=True)