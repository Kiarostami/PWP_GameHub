from flask import (
    Blueprint, jsonify
)


from API.db import get_list_of_all_games
from API.db import get_game_by_name_or_id


bp = Blueprint("game", __name__)


@bp.route("/games", methods=['GET'])
def get_games():
    gl = get_list_of_all_games()
    return jsonify({"status": 'ok', 'payload': str(gl)})


@bp.route("/games/<string:name_or_id>", methods=["GET"])
def get_game(name_or_id):
    game_to_return = get_game_by_name_or_id(name_or_id)
    if game_to_return:
        return jsonify({"status": 'ok', 'payload': str(game_to_return)})
    return  jsonify({"status": 'not found'})
