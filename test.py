import requests
from engine.game import Game
from entities.move import Move
from entities.position import Position
import pickle
import base64
BASE = 'http://127.0.0.1:5000'

def obj_to_bytes(obj):
    return pickle.dumps(obj)

def obj_to_json(obj):
    return base64.b64encode(obj_to_bytes(obj)).decode('utf-8')

def json_to_obj(json_bytes):
    return bytes_to_obj(base64.b64decode(json_bytes))

def bytes_to_obj(bytes):
    return pickle.loads(bytes)


response = requests.get(BASE + "/createGame/")
move = Move(Position(4, 1), Position(4, 3))
response = requests.post(BASE + "/makeMove/", {'game_id': 0, 'move': obj_to_json(move)})
print(response.json())

move = Move(Position(4, 6), Position(4, 5))
response = requests.post(BASE + "/makeMove/", {'game_id': 0, 'move': obj_to_json(move)})
print(response.json())

response = requests.get(BASE + "/getPossibleMoves/", {'game_id': 0})
moves = json_to_obj(response.json()['possibleMoves'])
print(moves)
