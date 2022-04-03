from crypt import methods
from flask import (
    Blueprint, jsonify, session
)


from api.db import get_list_of_all_games
from api.db import get_game_by_name_or_id
from api.db import add_game_to_list


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
    return jsonify({"status": 'not found'})


@bp.route("/games/add/<int:game_id>", methods=["POST"])
def add_game(game_id):
    user_id = session['id']
    agtl = add_game_to_list(user_id, game_id)
    return jsonify({"status": agtl}) 
