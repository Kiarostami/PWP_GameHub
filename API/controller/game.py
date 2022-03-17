from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from API.db import get_list_of_all_games
from API.db import get_game_by_name_or_id

from API.models import Game

bp = Blueprint("game", __name__)


@bp.route("/games", methods=['GET'])
def getGames():
    gl = get_list_of_all_games()
    return jsonify({"status": 'ok', 'payload': str(gl)})


@bp.route("/games/<string:nameOrId>", methods=["GET"])
def getGame(nameOrId):
    g = get_game_by_name_or_id(nameOrId)
    if g:
        return jsonify({"status": 'ok', 'payload': str(g)})
    return  jsonify({"status": 'not found'})

