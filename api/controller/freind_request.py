from flask import (Blueprint, jsonify, session)

from api.db import get_sent_friend_requests_by_user_id
from api.db import get_received_friend_requests_by_user_id
from api.db import add_friend_req
from api.db import delete_friend_req
from api.db import accept_friend_request

bp = Blueprint("friend_request", __name__, url_prefix="/fr")


@bp.route("/sent", methods=["GET"])
def get_sent_friend_reqs():
    user_id = session['id']
    fr = get_sent_friend_requests_by_user_id(user_id)
    return jsonify({'status': 'ok', "payload": fr})


@bp.route("/received", methods=["GET"])
def get_received_friend_reqs():
    user_id = session['id']
    fr = get_received_friend_requests_by_user_id(user_id)
    return jsonify({'status': 'ok', "payload": fr})


@bp.route("/<int:target_user_id>", methods=["POST"])
def add_friend(target_user_id: int):
    user_id = session['id']
    afr = add_friend_req(user_id, target_user_id)
    return jsonify({"status": afr})


@bp.route("/<int:fr_id>", methods=["DELETE"])
def reject_friend(fr_id: int):
    user_id = session['id']

    dfr = delete_friend_req(fr_id, user_id)
    return jsonify({"status": dfr})


@bp.route("/<int:fr_id>", methods=["PUT"])
def accept_friend(fr_id: int):
    user_id = session['id']
    afr = accept_friend_request(fr_id, user_id)
    return jsonify({"status": afr})