from flask import (
    Blueprint, jsonify, session
)

from API.db import get_list_of_games_per_user
from API.db import get_list_of_friends
from API.db import get_user_profile
from API.db import get_user_by_id
from API.db import get_user_by_name
from API.db import add_profile
from API.db import update_profile_status

from API.models import User

bp = Blueprint("user", __name__)


@bp.route("/user/<int:uid>", methods=['GET'])
def get_user_info_by_id(uid: int):
    u = get_user_by_id(uid)
    if type(u) == User:
        return jsonify({"status": 'ok', 'payload': u.protected()})
    return jsonify({"status": u})


@bp.route("/user/uname/<string:name>", methods=['GET'])
def get_user_info_by_name(name: str):
    u = get_user_by_name(name)
    if type(u) == User:
        return jsonify({"status": 'ok', 'payload': u.protected()})
    return jsonify({"status": u})


@bp.route("/getGameList", methods=["GET"])
def get_users_game():
    user_id = session['id']
    gl = get_list_of_games_per_user(user_id)
    return jsonify({"status": "ok", 'payload': gl})


@bp.route("/getFriends", methods=["GET"])
def get_friends_list():
    user_id = session['id']
    fl = get_list_of_friends(user_id)
    return jsonify({"status": "ok", "payload": fl})


@bp.route("/profile", methods=["GET"])
def get_profile():
    user_id = session['id']
    p = get_user_profile(user_id)
    if p[0] != "ok":
        return jsonify({'status': 'invalid'})
    return jsonify({'status': 'ok', 'payload': p[1]})


@bp.route("/add_profile/<string:bio>/<string:status>", methods=["POST"])
def add_user_profile(bio, status):
    username = session['user']
    res = add_profile(username, bio, status)
    return jsonify({'status': res}) 

@bp.route("/update_status/<string:status>", methods=["PUT"])
def update_user_profile(status):
    user_id = session['id']
    update_profile_status(user_id, status)
    return jsonify({"status": "ok"}) 