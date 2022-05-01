from flask import (
    Blueprint, jsonify, request
)

from flask_jwt_extended import (jwt_required, get_jwt_identity
)
from api.db import add_game_to_list
from api.db import check_user_has_game 
from api.db import get_game_by_name_or_id
from api.db import get_list_of_games_per_user
from api.db import get_list_of_friends
from api.db import get_user_profile
from api.db import get_user_by_id
from api.db import update_profile_bio
from api.db import add_profile
from api.db import update_profile_status

from api.models import User

bp = Blueprint("user", __name__)


@bp.route("/user/<int:user_id>", methods=['GET'])
@jwt_required()
def get_user_info_by_id(user_id: int):
    """Get user info by id.
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
        User:
            type: object
            properties:
                id:
                    type: integer
                    example: 1
                username:
                    type: string
                    example: "test"
                email:
                    type: string
                    example: "test@test.com"
                avatar:
                    type: string
                    example: "test.jpg"
    responses:
        200:
            description: Ok
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: object
                        properties:
                            id:
                                type: integer
                                example: 1
                            username:
                                type: string
                                example: "test"
        400:
            description: Bad request
        404:
            description: User not found

    """
    response = {
        "status": "",
        "payload": {},
    }
    user = get_user_by_id(user_id)
    if type(user) == User:
        response["status"] = "ok"
        response["payload"] = user.protected()
        return jsonify(response), 200
    else:
        response["status"] = "not found"
        return jsonify(response), 404


@bp.route("/user/<int:uid>/profile", methods=["GET"])
@jwt_required()
def get_profile(uid):
    """Returns the profile of a user by their id.
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
        Profile:
            type: object
            properties:
                id:
                    type: integer
                    example: 1
                user_id:
                    type: integer
                    example: 1
                bio:
                    type: string
                    example: "I am a test user"
                status:
                    type: string
                    example: "online"
                background:
                    type: string
                    example: "test.jpg"
    responses:
        200:
            description: "Ok"
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: object
                        $ref: "#/definitions/Profile"
        400:
            description: "Bad request"
        404:
            description: "User not found"
    """
    response = {
        "status": "",
        "payload": {},
    }
    
    profile = get_user_profile(uid)
    if profile[0] != "ok":
        response["status"] = profile[0]
        return jsonify(response), 404
    response["status"] = "ok"
    response["payload"] = profile[1].__dict__
    return jsonify(response), 200


@bp.route("/user/<int:uid>/friends", methods=["GET"])
@jwt_required()
def get_users_friends(uid):
    """Returns the friends of a user by their id.
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
    responses:
        200:
            description: "Ok"
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: array
                        items:
                            $ref: "#/definitions/User"
        400:
            description: "Bad request"
        404:
            description: "User not found"
    """
    response = {
        "status": "",
        "payload": {},
    }
    friends_list = get_list_of_friends(uid)
    if friends_list:
        response["status"] = "ok"
        response["payload"] = friends_list
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/user/<int:user_id>/profile", methods=["POST"])
@jwt_required()
def add_user_profile(user_id):
    """Adds a new profile to a user.
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
      description: "the status and bio of the user"
      schema:
        type: object
        properties:
            bio:
                type: string
                example: "I am a test user"
            status:
                type: string
                example: "online"
    responses:
        200:
            description: "Ok"
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
            description: "User not found"

    """
    response = {
        "status": "",
        "payload": {},
    }
    # check if user_id matches the id of the user in the token
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
    
    # check bio and status exist in request body
    if "bio" not in request.json or "status" not in request.json:
        response["status"] = "bad request"
        return jsonify(response), 400

    # check if profile already exists
    profile = get_user_profile(user_id)
    if profile[0] == "ok":
        response["status"] = "profile already exists"
        return jsonify(response), 400

    # check bio and status exist in request body
    if "bio" not in request.json or "status" not in request.json:
        response["status"] = "bad request"
        return jsonify(response), 400
    bio = request.json["bio"]
    status = request.json["status"]

    # add profile
    add_profile(user_id, bio, status)
    response["status"] = "ok"
    return jsonify(response), 200


@bp.route("/user/<int:user_id>/profile", methods=["PUT"])
@jwt_required()
def update_user_profile(user_id):
    """"Updates the status or bio of a user.
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
      description: "the status and bio of the user"
      schema:
        type: object
        properties:
            bio:
                type: string
                example: "I am a test user"
            status:
                type: string
                example: "online"
    responses:
        200:
            description: "Ok"
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
            description: "User not found"
    """
    response = {
        "status": "",
        "payload": {},
    }

    # check if uid matches the id of the user in the token
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
        
    # check if profile already exists
    profile = get_user_profile(user_id)
    if profile[0] != "ok":
        response["status"] = "profile does not exist"
        return jsonify(response), 404

    flag = 0
    if "bio" in request.json:
        bio = request.json["bio"]
        update_profile_bio(user_id, bio)
        flag = 1
    if "status" in request.json:
        status = request.json["status"]
        update_profile_status(user_id, status)
        flag = 1
    
    if flag:
        response["status"] = "ok"
        return jsonify(response), 200
    response["status"] = "bad request"
    return jsonify(response), 400


@bp.route("/user/<int:user_id>/games", methods=["GET"])
@jwt_required()
def get_users_games(user_id):
    """Returns the games of a user by their id.
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
    responses:
        200:
            description: "Ok"
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: array
                        items:
                            $ref: "#/definitions/Game"
        404:
            description: "Not found"
    """
    response = {
        "status": "",
        "payload": {},
    }
    games_list = get_list_of_games_per_user(user_id)
    if games_list:
        response["status"] = "ok"
        response["payload"] = games_list
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/user/<int:user_id>/games", methods=["POST"])
@jwt_required()
def add_game_to_user(user_id):
    """Add a game to a user and returns the status of the request.
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
      description: "The game to add to the user"
      schema:
        type: object
        properties:
            game_id:
                type: integer
                example: 1
    responses:
        200:
            description: "Ok"
        400:
            description: "Bad request"
        401:
            description: "Unauthorized"
        404:
            description: "Not found"
    """
    response = {
        "status": "",
        "payload": {},
    }

    # check if uid matches the id of the user in the token
    if user_id != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
    
    # check the game_id exists in request body
    if "game_id" not in request.json:
        response["status"] = "bad request"
        return jsonify(response), 400
    game_id = request.json["game_id"]

    # check if game already exists
    game = get_game_by_name_or_id(game_id)
    if game == None:
        response["status"] = "game does not exist"
        return jsonify(response), 404

    # check if user already has game
    user_game = check_user_has_game(user_id, game_id)
    if user_game:
        response["status"] = "user already has game"
        return jsonify(response), 400

    # add game to user
    res = add_game_to_list(user_id, game_id)
    response["status"] = res
    return jsonify(response), 200
