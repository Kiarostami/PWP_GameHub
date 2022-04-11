from flask import (Blueprint, jsonify, request)
from datetime import datetime

from flask_jwt_extended import (jwt_required, get_jwt_identity)


from api.db import get_game_by_name_or_id, get_invite_from_others_message, get_user_by_id
from api.db import get_invite_to_others_message
from api.db import get_invite_msg_by_id
from api.db import update_invite_msg_by_id
from api.db import create_invite_msg
from api.db import delete_invite_msg


from api.models import InviteMessage


bp = Blueprint("invite_message", __name__, url_prefix="/invitation")

@bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_invite_message(user_id):
    """
    Get all the invitation of a user.
    :param user_id:
    :return:
        json: list of invitation

    """
    response = {
        "status": "",
        "payload": {}
    }

    # check user authorization
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
    
    inv_list1 = get_invite_from_others_message(user_id)
    inv_list2 = get_invite_to_others_message(user_id)
    result = inv_list1 + inv_list2
    if result:
        response["status"] = "success"
        response["payload"] = result
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/<int:user_id>", methods=["POST"])
@jwt_required()
def create_invite_message(user_id):
    """
    Create a new invitation.
    :param user_id:
    :return:
        json: invitation
    """
    response = {
        "status": "",
        "payload": {}
    }

    # check user authorization
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if the request body is empty
    if not request.json:
        response["status"] = "bad request"
        return jsonify(response), 400

    # check if the request body is valid
    if not all(key in request.json for key in ("game_id", "receiver_id", "suggestedTime")):
        response["status"] = "bad request"
        return jsonify(response), 400

    # check if the game_id is valid
    if get_game_by_name_or_id(request.json["game_id"]) == None:
        response["status"] = "game not exists"
        return jsonify(response), 404

    # check if the receiver_id is valid
    if get_user_by_id(request.json["receiver_id"]) == "not found":
        response["status"] = "user not exists"
        return jsonify(response), 404
        

    inv_msg = InviteMessage(None, request.json["game_id"],
                            user_id, request.json["receiver_id"], 
                            request.json["suggestedTime"],
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            )
    create_invite_msg(inv_msg)
    response["status"] = "ok"
    return jsonify(response), 201


@bp.route("/<int:user_id>/<int:invite_id>", methods=["DELETE"])
@jwt_required()
def delete_invite_message(user_id, invite_id):
    """
    Delete an invitation.
    :param user_id:
    :param invite_id:
    :return:
        json: status
    """
    response = {
        "status": "",
        "payload": {}
    }

    # check user authorization
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if the invitation is valid
    if get_invite_msg_by_id(invite_id) == "not found":
        response["status"] = "bad request"
        return jsonify(response), 400

    delete_invite_msg(invite_id)
    response["status"] = "ok"
    return jsonify(response), 200


@bp.route("/<int:user_id>/<int:invite_id>", methods=["PUT"])
@jwt_required()
def update_invite_message(user_id, invite_id):
    """Update an inviation message by values of accepted = True 
       or False in request.json
       :parameters:
            - user_id: int id of the user
            - invite_id: int id of the invitation
       :return:
            json: status
    """
    response = {
        "status": "",
        "payload": {}
    }

    # check user authorization
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if the invitation is valid
    if get_invite_msg_by_id(invite_id) == "not found":
        response["status"] = "bad request"
        return jsonify(response), 400

    # check if the request body is empty
    if not request.json:
        response["status"] = "bad request"
        return jsonify(response), 400

    # check if the request body is valid
    if not all(key in request.json for key in ("accepted")):
        response["status"] = "bad request"
        return jsonify(response), 400

    # check if the accepted is valid
    if not isinstance(request.json["accepted"], bool):
        response["status"] = "bad request"
        return jsonify(response), 400

    update_invite_msg_by_id(invite_id, request.json["accepted"])
    response["status"] = "ok"
    return jsonify(response), 200
    