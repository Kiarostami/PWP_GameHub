import json
from flask import (Blueprint, jsonify, Response, request)
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from api.db import delete_friend_from_friend_list
from api.db import get_sent_friend_requests_by_user_id
from api.db import get_user_by_id
from api.db import get_received_friend_requests_by_user_id
from api.db import add_friend_req
from api.db import delete_friend_req
from api.db import accept_friend_request

from api.util import MASON_TYPE

bp = Blueprint("friend_request", __name__, url_prefix="/friends")


@bp.route("/<int:user_id>/pending", methods=["GET"])
@jwt_required()
def get_pending_friend_requests(user_id):
    """
    Get all pending friend requests for a user from others
    ---
    produces:
    - "application/json"
    - "application/vnd.mason+json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    definitions:
      FriendRequestWithCtrl:
        type: object
        properties:
            id:
                type: integer
                example: 1
            sender_id:
                type: integer
                example: 1
            receiver_id:
                type: integer
                example: 2
            creationTime:
                type: string
                example: "2020-01-01T00:00:00"
            "@controls":
                type: object
                properties:
                    accept:
                        type: object
                        properties:
                            href:
                                type: string
                                example: "/friends/4/accept/3"
                            method:
                                type: string
                                example: "POST"
                                title: "Accept friend request"
                    decline:
                        type: object
                        properties:
                            href:
                                type: string
                                example: "/friends/4/reject/3"
                            method:
                                type: string
                                example: "DELETE"
                            title: "Decline friend request"
    responses:
        200:
            description: "success retrieving pending friend requests"
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: array
                        items:
                            $ref: "#/definitions/FriendRequestWithCtrl"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"   

    """
    response = {
        "status": "",
        "payload": {}
    }
    print(request.headers)
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    received_friend_requests = get_received_friend_requests_by_user_id(user_id)
    if received_friend_requests:
        response["status"] = "ok"
        for index in range(len(received_friend_requests)):
            received_friend_requests[index] = received_friend_requests[index].serialize()

        response["payload"] = received_friend_requests
        return Response(json.dumps(response), status=200, mimetype=MASON_TYPE)
        
    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/<int:user_id>/sent", methods=["GET"])
@jwt_required()
def get_sent_friend_requests(user_id):
    """Returns all the friend requests sent by this user to others
    ---
    produces:
    - "application/json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    definitions:
        FriendRequest:
            type: object
            properties:
                id:
                    type: integer
                    example: 1
                sender_id:
                    type: integer
                    example: 1
                receiver_id:
                    type: integer
                    example: 2
                creationTime:
                    type: string
                    example: "2020-01-01T00:00:00"
    responses:
        200:
            description: "success retrieving sent friend requests"
            schema:
                $ref: "#/definitions/FriendRequest"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
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
    

@bp.route("/<int:user_id>", methods=["POST"])
@jwt_required()
def add_friend_request(user_id):
    """Adds a friend request to the database.
    ---
    produces:
    - "application/json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    - name: body
      in: body
      description: "The target user_id"
      required: true
      schema:
        type: object
        properties:
            user2_id:
                type: integer
                example: 2
    responses:
        200:
            description: "success adding friend request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
        400:
            description: "Bad request"
    """
    response = {
        "status": "",
        "payload": {}
    }
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
    if "user2_id" not in request.json:
        response["status"] = "bad request"
        return jsonify(response), 400

    user2_id = request.json["user2_id"]
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
    ---
    produces:
    - "application/json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    - name: friend_request_id
      in: path
      description: "Friend request's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    responses:
        200:
            description: "success accepting friend request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
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
    ---
    produces:
    - "application/json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    - name: friend_request_id
      in: path
      description: "Friend request's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    responses:
        200:
            description: "success accepting friend request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
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
    ---
    produces:
    - "application/json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    - name: user2_id
      in: path
      description: "Target user's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 2
    responses:
        200:
            description: "success removing friend"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"

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
    ---
    produces:
    - "application/json"
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: user_id
      in: path
      description: "User's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 1
    - name: friend_request_id
      in: path
      description: "Friend request's id"
      required: true
      type: integer
      schema:
        type: integer
        example: 10
    responses:
        200:
            description: "success rejecting friend request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
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
