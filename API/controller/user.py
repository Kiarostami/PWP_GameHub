from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from API.db import add_user
from API.db import add_profile
from API.db import get_list_of_games
from API.db import get_list_of_friends
from API.db import get_user_profile
from API.db import get_pending_friend_request
from API.db import get_receiving_friend_request
from API.db import get_invite_from_others_message
from API.db import get_invite_to_others_message

from API.models import User

bp = Blueprint("user", __name__)


@bp.route("/getGameList", methods=["GET"])
def getUsersGame():
    user_id = session['id']
    gl = get_list_of_games(user_id)
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

@bp.route("/getFrndsMsg")
def get_other_inv_msg():
    user_id = session['id']
    m = get_invite_from_others_message(user_id)
    return jsonify({'status': 'ok', 'payload': m})


@bp.route("/getUsrMsg")
def get_user_inv_msg():
    user_id = session['id']
    m = get_invite_to_others_message(user_id)
    return jsonify({'status': 'ok', 'payload': m})


