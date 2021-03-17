from application.handlers.create_game import CreateGame
from application.handlers.make_move import MakeMove
from application.handlers.get_game_details import GetGameDetails
from flask import Flask
from flask_restful import Api

from .extensions import db


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    return None


def create_app(config_object=".settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    register_extensions(app)
    api = Api(app)
    api.add_resource(CreateGame, "/createGame/")
    api.add_resource(MakeMove, "/makeMove/")
    api.add_resource(GetGameDetails, "/getGameDetails/")
    return app
