from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from API.db import add_user
from API.db import add_profile
from API.db import get_list_of_games_per_user
from API.db import get_list_of_friends
from API.db import get_user_profile
from API.db import get_pending_friend_request
from API.db import get_receiving_friend_request
from API.db import get_user_by_id
from API.db import get_user_by_name

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
def getUsersGame():
    user_id = session['id']
    gl = get_list_of_games_per_user(user_id)
    return jsonify({"status": "OK", 'payload': str(gl)})


@bp.route("/getFriends", methods=["GET"])
def getFrindsList():
    user_id = session['id']
    fl = get_list_of_friends(user_id)
    return jsonify({"status": "ok", "payload": fl})


@bp.route("/profile", methods=["GET"])
def getProfile():
    user_id = session['id']
    p = get_user_profile(user_id)
    if p[0] != "OK":
        return jsonify({'status': 'invalid'})
    return jsonify({'status': 'ok', 'payload': str(p[1])})


@bp.route("/getFrndReq", methods=['GET'])
def getFriendRequest():
    user_id = session['id']
    fr = get_receiving_friend_request(user_id)
    return jsonify({'status': 'ok', 'payload': str(fr)})


@bp.route("/getPendingFrndReq", methods=["GET"])
def getPendingFrReq():
    user_id = session['id']
    fr = get_pending_friend_request(user_id)
    return jsonify({'status': 'ok', 'payload': str(fr)})


@bp.route("/upProf", methods=["POST"])
def update_profile():
    pass