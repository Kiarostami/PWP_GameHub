from flask import (
    Blueprint, jsonify
)

from flask_jwt_extended import (jwt_required)


from api.cache import cache

from api.db import get_game_by_name_or_id
from api.db import get_game_genres_list


bp = Blueprint("genres", __name__)

@bp.route("/genres/<int:game_id>", methods=["GET"])
@jwt_required()
def get_genres(game_id):
    """"Return all genres of a game
    :parameters:
        - game_id: int
    :return:
        list of all genres for a game
    """
    response = {
        "status": "",
        "payload": {},
    }

    game_to_return = get_game_by_name_or_id(game_id)
    if game_to_return:
        response["status"] = "ok"
        response["payload"] = get_game_genres_list(game_id)
        for index in range(len(response["payload"])):
            response["payload"][index] = response["payload"][index].serialize()
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404