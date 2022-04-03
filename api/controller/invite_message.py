from flask import (Blueprint, jsonify, session)
from datetime import datetime


from api.db import get_invite_from_others_message
from api.db import get_invite_to_others_message
from api.db import get_invite_msg_by_id
from api.db import update_invite_msg_by_id
from api.db import create_invite_msg
from api.db import delete_invite_msg


from api.models import InviteMessage


bp = Blueprint("invite_message", __name__, url_prefix="/im")

@bp.route("/self", methods=["GET"])
def self_msgs():
    user_id = session['id']
    gifom = get_invite_from_others_message(user_id)
    return jsonify({"status": "ok", 'payload': gifom})

@bp.route("/others", methods=["GET"])
def others_msgs():
    user_id = session['id']
    gitom = get_invite_to_others_message(user_id)
    return  jsonify({"status": "ok", 'payload': gitom})

@bp.route("/<int:msg_id>", methods=["GET"])
def get_msg(msg_id: int):
    user_id = session['id']
    msg = get_invite_msg_by_id(msg_id)
    if msg:
        if user_id == msg.receiver_id or user_id == msg.sender_id:
            return jsonify({"status": 'ok', 'payloda': msg.__dict__})
        return jsonify({"status": 'invalid'})

    return  jsonify({"status": 'not found'})

@bp.route("/accmsg/<int:msg_id>", methods=["PUT"])
def accept_inv(msg_id: int):
    user_id = session['id']
    msg = get_invite_msg_by_id(msg_id)
    if msg:
        if user_id == msg.receiver_id:
            msg = update_invite_msg_by_id(msg_id, True)
            return jsonify({"status": 'ok', 'payloda': msg.__dict__})
        return jsonify({"status": 'invalid'})

    return jsonify({"status": 'not found'})


@bp.route("/rejmsg/<int:msg_id>", methods=["PUT"])
def reject_inv(msg_id: int):
    user_id = session['id']
    msg = get_invite_msg_by_id(msg_id)
    if msg:
        if user_id == msg.receiver_id:
            msg = update_invite_msg_by_id(msg_id, False)
            return jsonify({"status": 'ok', 'payloda': msg.__dict__})
        return jsonify({"status": 'invalid'})

    return jsonify({"status": 'not found'})


@bp.route("/crtinv/<int:game_id>/<int:receiver_id>/<string:suggested_time>", methods=['POST'])
def create_inv(game_id: int, receiver_id: int, suggested_time: str):
    user_id = session['id']
    ct = datetime.now()
    im = InviteMessage(None, game_id, user_id, receiver_id, suggested_time, ct)
    create_invite_msg(im)

    return jsonify({'status': 'ok'})

@bp.route("/delinv/<int:msg_id>", methods=['DELETE'])
def delete_inv(msg_id: int):
    user_id = session['id']
    msg = get_invite_msg_by_id(msg_id)
    if msg:
        if user_id == msg.sender_id:
            delete_invite_msg(msg_id)
            return jsonify({"status": "ok"})
        return jsonify({"status": 'invalid'})
    return jsonify({"status": 'not found'}) 
