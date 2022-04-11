from flask import (Blueprint, jsonify)
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from api.db import delete_friend_from_friend_list
from api.db import get_sent_friend_requests_by_user_id
from api.db import get_user_by_id
from api.db import get_received_friend_requests_by_user_id
from api.db import add_friend_req
from api.db import delete_friend_req
from api.db import accept_friend_request

bp = Blueprint("friend_request", __name__, url_prefix="/friends")


@bp.route("/<int:user_id>/pending", methods=["GET"])
@jwt_required()
def get_pending_friend_requests(user_id):
    """
    Get all pending friend requests for a user from others
    :parameters:
        - user_id: int
    :return:
        - status: int
        - payload: list of friend requests
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    received_friend_requests = get_received_friend_requests_by_user_id(user_id)
    if received_friend_requests:
        response["status"] = "ok"
        response["payload"] = received_friend_requests
        return jsonify(response), 200
    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/<int:user_id>/sent", methods=["GET"])
@jwt_required()
def get_sent_friend_requests(user_id):
    """Returns all the friend requests sent by this user to others
    :parameters:
        - user_id: int
    :return:
        - status: int
        - payload: list of friend requests
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    sent_friend_requests = get_sent_friend_requests_by_user_id(user_id)
    if sent_friend_requests:
        response["status"] = "ok"
        response["payload"] = sent_friend_requests
        return jsonify(response), 200
    response["status"] = "not found"
    return jsonify(response), 404
    

@bp.route("/<int:user_id>/<int:user2_id>", methods=["POST"])
@jwt_required()
def add_friend_request(user_id, user2_id):
    """"Adds a friend request to the database.
    :parameters:
        - user_id: int
        - user2_id: int
    :return:
        - status: string
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
    
    # check user2 exists
    if get_user_by_id(user2_id) == "not found":
        response["status"] = "user does not exist"
        return jsonify(response), 404

    friend_request = add_friend_req(user_id, user2_id)

    response["status"] = friend_request
    return jsonify(response), 200

    
@bp.route("/<int:user_id>/accept/<int:friend_request_id>", methods=["POST"])
@jwt_required()
def accept_friend_request_api(user_id, friend_request_id):
    """User accepts a friend request.
    :parameters:
        :param user_id: int
        :param friend_request_id: int
    :return:
        - status: string
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    friend_request = accept_friend_request(user_id, friend_request_id)

    if friend_request == "accepted":
        response["status"] = "accepted"
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/<int:user_id>/cancel/<int:friend_request_id>", methods=["DELETE"])
@jwt_required()
def cancel_friend_request_api(user_id, friend_request_id):
    """cancel a pending a friend request by the user.
    :parameters:
        - user_id: int
        - friend_request_id: int
    :return:
        - status: string
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    friend_request = delete_friend_req(user_id, friend_request_id)

    if friend_request == "ok":
        response["status"] = "deleted"
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404
    

@bp.route("/<int:user_id>/remove/<int:user2_id>", methods=["DELETE"])
@jwt_required()
def remove_a_friend(user_id, user2_id):
    """Remove a friend from the friends list.
    :parameters:
        - user_id: int
        - user2_id: int
    :return:
        - status: string
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    friend_request = delete_friend_from_friend_list(user_id, user2_id)

    if friend_request == "ok":
        response["status"] = "deleted"
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/<int:user_id>/reject/<int:friend_request_id>", methods=["DELETE"])
@jwt_required()
def reject_friend_request_api(user_id, friend_request_id):
    """User rejects a friend request.
    :parameters:
        - user_id: int
        - friend_request_id: int
    :return:
        - status: string
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    friend_request = delete_friend_req(user_id, friend_request_id)

    if friend_request == "ok":
        response["status"] = "deleted"
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404
