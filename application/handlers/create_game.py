
from typing import Dict

from application.games_storage import games_storage_singleton

from flask_restful import Resource


class CreateGame(Resource):
    def get(self) -> Dict[str, str]:
        id, _ = games_storage_singleton.create_new_game()
        return {
            'id': id,
        }
