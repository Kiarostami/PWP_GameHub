from flask import (Blueprint, jsonify, request)
from datetime import datetime

from flask_jwt_extended import (jwt_required, get_jwt_identity)

from jsonschema import validate, ValidationError


from api.db import get_game_by_name_or_id, get_invite_from_others_message, get_user_by_id, validate_invitation_receiver
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
      required: true
      description: "The id of the user"
      type: integer
      example: 1
    definitions:
        InviteMessage:
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
                game_id:
                    type: integer
                    example: 3
                suggestedTime:
                    type: string
                    example: "2020-01-01 00:00:00"
                createdTime:
                    type: string
                    example: "2020-01-01 00:00:00"
                accepted:
                    type: boolean
                    example: false
    responses:
        200:
            description: "Success" 
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: array
                        items:
                            $ref: '#/definitions/InviteMessage'
        400:
            description: "Bad request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
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
      required: true
      description: "The id of the user"
      type: integer
      example: 1
    - name: body
      in: body
      required: true
      description: "The invitation message"
      schema:
        $ref: '#/definitions/InviteMessage'
    responses:
        201:
            description: "Created"
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
        400:
            description: "Bad request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
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
    try:
        validate(request.json, InviteMessage.new_json_schema())
    except ValidationError as e:
        response["status"] = "bad request"
        response["payload"] = e.message
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


@bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_invite_message(user_id):
    """
    Delete an invitation.
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
      required: true
      description: "The id of the user"
      type: integer
      example: 1
    - name: body
      in: body
      required: true
      description: "The invitation message"
      schema:
        type: object
        properties:
            invite_id:
                type: integer
                example: 1
    responses:
        200:
            description: "Success"
        400:
            description: "Bad request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
    """
    response = {
        "status": "",
        "payload": {}
    }

    # check user authorization
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if invite_id is in request body
    if "invite_id" not in request.json:
        response["status"] = "bad request"
        return jsonify(response), 400

    invite_id = request.json["invite_id"]

    # check if the invitation is valid
    if get_invite_msg_by_id(invite_id) == None:
        response["status"] = "invitation not exists"
        return jsonify(response), 404

    # check if the invitation is from the user
    if not (get_invite_msg_by_id(invite_id).receiver_id == user_id or 
            get_invite_msg_by_id(invite_id).sender_id == user_id):
        response["status"] = "unauthorized"
        return jsonify(response), 401

    delete_invite_msg(invite_id)
    response["status"] = "ok"
    return jsonify(response), 200


@bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_invite_message(user_id):
    """Update an inviation message by values of accepted = True 
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
      required: true
      description: "The id of the user"
      type: integer
      example: 1
    - name: body
      in: body
      required: true
      description: "The invitation message id"
      schema:
        type: object
        properties:
            invite_id:
                type: integer
                example: 1
            accepted:
                type: boolean
                example: True

    responses:
        200:
            description: "Success"
        400:
            description: "Bad request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
    """
    response = {
        "status": "",
        "payload": {}
    }
    
    # check user authorization
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if invite_id is in request body
    if "invite_id" not in request.json:
        response["status"] = "bad request"
        return jsonify(response), 400

    invite_id = request.json["invite_id"]

    # check if the invitation is valid
    if get_invite_msg_by_id(invite_id) == None:
        response["status"] = "not found"
        return jsonify(response), 404

    # check if the request body is valid
    if not request.json.get("accepted", False):
        response["status"] = "body has no key accepted"
        return jsonify(response), 400

    # check if the accepted is valid
    if not isinstance(request.json["accepted"], bool):
        response["status"] = "accepted is not a boolean"
        return jsonify(response), 400

    # validate receiver
    if not validate_invitation_receiver(user_id, invite_id):
        response["status"] = "invalid receiver"
        return jsonify(response), 400

    update_invite_msg_by_id(invite_id, request.json["accepted"])
    response["status"] = "ok"
    return jsonify(response), 200
    