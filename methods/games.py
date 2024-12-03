from models import Game
from .exceptions import *


def get_game_by_id(game_id):
    game = Game.query.get(game_id)

    if not game:
        raise NotFound

    return game


def get_game_by_code(game_code):
    game = Game.query.filter_by(code=game_code).first()

    if not game:
        raise NotFound

    return game


def get_games():
    return Game.query.all()
