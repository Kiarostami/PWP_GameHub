from flask import (
    Blueprint, jsonify
)

from flask_jwt_extended import (jwt_required, get_jwt_identity
)

from api.db import add_game_to_list, check_user_has_game, get_game_by_name_or_id, get_list_of_games_per_user
from api.db import get_list_of_friends
from api.db import get_user_profile
from api.db import get_user_by_id
from api.db import update_profile_bio
from api.db import add_profile
from api.db import update_profile_status

from api.models import User

bp = Blueprint("user", __name__)


@bp.route("/user/<int:uid>", methods=['GET'])
@jwt_required()
def get_user_info_by_id(uid: int):
    """Get user info by id.
    :param uid: user id
    :return: json user info
    """
    response = {
        "status": "",
        "payload": {},
    }
    user = get_user_by_id(uid)
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
    :parameters:
        uid: int
            The id of the user to get the profile of.
    :returns:
        json:
            A json object containing the status of the request, the payload
            and the access token.
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
    :parameters:
        uid: int
            The id of the user to get the friends of.
    :returns:
        json:
            A json object containing the list of the friends in the payload.
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


@bp.route("/user/<int:uid>/profile/<string:bio>/<string:status>", methods=["POST"])
@jwt_required()
def add_user_profile(uid, bio, status):
    """Adds a profile to a user.
    :parameters:
        uid: int
            The id of the user to add the profile to.
        bio: string
            The bio of the user.
        status: string
            The status of the user.
    :returns:
        json:
            A json object containing the status of the request.
    """
    response = {
        "status": "",
        "payload": {},
    }
    # check if uid matches the id of the user in the token
    if uid != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if profile already exists
    profile = get_user_profile(uid)
    if profile[0] == "ok":
        response["status"] = "profile already exists"
        return jsonify(response), 400
    # add profile
    add_profile(uid, bio, status)
    response["status"] = "ok"
    return jsonify(response), 200


@bp.route("/user/<int:uid>/profile/status/<string:new_status>", methods=["PUT"])
@jwt_required()
def update_user_profile_status(uid, new_status):
    """"Updates the status of a user.
    :parameters:
        uid: int
            The id of the user to update the status of.
        new_status: string
            The new status of the user.
    :returns:
        json:
            A json object containing the status of the request.
    """
    response = {
        "status": "",
        "payload": {},
    }

    # check if uid matches the id of the user in the token
    if uid != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
        
    # check if profile already exists
    profile = get_user_profile(uid)
    if profile[0] != "ok":
        response["status"] = "profile does not exist"
        return jsonify(response), 404

    # update profile status
    res = update_profile_status(uid, new_status)
    response["status"] = res
    return jsonify(response), 200



@bp.route("/user/<int:uid>/profile/bio/<string:new_bio>", methods=["PUT"])
@jwt_required()
def update_user_profile_bio(uid, new_bio):
    """"Updates the bio of a user.
    :parameters:
        uid: int
            The id of the user to update the bio of.
        new_bio: string
            The new bio of the user.
    :returns:
        json:
            A json object containing the status of the request.
    """
    response = {
        "status": "",
        "payload": {},
    }

    # check if uid matches the id of the user in the token
    if uid != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401
        
    # check if profile already exists
    profile = get_user_profile(uid)
    if profile[0] != "ok":
        response["status"] = "profile does not exist"
        return jsonify(response), 404

    res = update_profile_bio(uid, new_bio)
    response["status"] = res
    return jsonify(response), 200


@bp.route("/user/<int:uid>/games", methods=["GET"])
@jwt_required()
def get_users_games(uid):
    """Returns the games of a user by their id.
    :parameters:
        uid: int
            The id of the user to get the games of.
    :returns:
        json:
            A json object containing the list of the games in the payload.
    """
    response = {
        "status": "",
        "payload": {},
    }
    games_list = get_list_of_games_per_user(uid)
    if games_list:
        response["status"] = "ok"
        response["payload"] = games_list
        return jsonify(response), 200

    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/user/<int:uid>/games/<int:gid>", methods=["POST"])
@jwt_required()
def add_game_to_user(uid, gid):
    """Add a game to a user and returns the status of the request.
    :parameters:
        uid: int
            The id of the user to add the game to.
        gid: int
            The id of the game to add to the user.
    :returns:
        json:
            A json object containing the status of the request.
    """
    response = {
        "status": "",
        "payload": {},
    }

    # check if uid matches the id of the user in the token
    if uid != get_jwt_identity()["id"]:
        response["status"] = "unauthorized"
        return jsonify(response), 401

    # check if game already exists
    game = get_game_by_name_or_id(gid)
    if game == None:
        response["status"] = "game does not exist"
        return jsonify(response), 404

    # check if user already has game
    user_game = check_user_has_game(uid, gid)
    if user_game:
        response["status"] = "user already has game"
        return jsonify(response), 400

    # add game to user
    res = add_game_to_list(uid, gid)
    response["status"] = res
    return jsonify(response), 200