import json
from flask import (
    Blueprint, jsonify, Response
)

from flask_jwt_extended import (jwt_required, get_jwt_identity)


from api.util import MASON_TYPE

from api.cache import cache

from api.db import get_game_by_name_or_id
from api.db import get_list_of_all_games


bp = Blueprint("games", __name__)


@bp.route("/games/<string:name_or_id>", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_game(name_or_id):
    """Returns the game by name or id.
    ---
    produces:
    - application/json
    - application/vnd.mason+json
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    - name: name_or_id
      in: path
      required: true
      description: "The name or id of the game"
      type: string
      example: "DOTA 2"
    definitions:
     GameWithCtrl:
        type: object
        properties:
            id:
                type: integer
                example: 1
            name:
                type: string
                example: "DOTA 2"
            publisher:
                type: string
                example: "Valve"
            description:
                type: string
                example: "DOTA 2 is a multiplayer ..."
            isFree:
                type: boolean
                example: 1
            price:
                type: integer
                example: 100
            "@control":
                type: object
                properties:
                    "gamehub:genres":
                        type: array
                        items:
                            type: object
                            properties:
                                href:
                                    type: string
                                    example: "/genres/1"
                    "gamehub:add_game":
                        type: object
                        properties:
                            href:
                                type: string
                                example: "/user/1/games/1"
                            method:
                                type: string
                                example: "POST"
                            encoding:
                                type: string
                                example: "application/json"
                            title:
                                type: string
                                example: "Add game"
     Game:
        type: object
        properties:
            id:
                type: integer
                example: 1
            name:
                type: string
                example: "DOTA 2"
            publisher:
                type: string
                example: "Valve"
            description:
                type: string
                example: "DOTA 2 is a multiplayer ..."
            isFree:
                type: boolean
                example: 1
            price:
                type: integer
                example: 100
        
    responses:
        200:
            description: the game and details
            schema:
                $ref: '#/definitions/GameWithCtrl'
        404:
            description: game not found
    """
    response = {
        "status": "",
        "payload": {},
    }
    user_id = get_jwt_identity()["id"]
    game_to_return = get_game_by_name_or_id(name_or_id)
    if game_to_return:
        response["status"] = "ok"
        response["payload"] = game_to_return.serialize(user_id)
        return Response(
                        json.dumps(response),
                        status=200, 
                        mimetype=MASON_TYPE
                        )
    response["status"] = "not found"
    return jsonify(response), 404


@bp.route("/games", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_all_games():
    """Returns all games.
    ---
    produces:
    - application/json
    parameters:
    - name: Authorization
      in: header
      description: "Bearer token"
      required: true
      type: string
      format: "Bearer <token>"
    responses:
        200:
            description: the list of all games
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: "ok"
                    payload:
                        type: array
                        items:
                            $ref: '#/definitions/Game'
        400:
            description: error
    """
    response = {
        "status": "",
        "payload": {},
    }
    
    response["status"] = "ok"
    response["payload"] = [game.__dict__ for game in get_list_of_all_games()]
    return jsonify(response), 200
