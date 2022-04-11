from flask import (
    Blueprint, g, request, jsonify
)

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from api.db import check_login
from api.db import add_user

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    response = {"status": "",
                "payload": {},
                "access_token": ""}

    if all(k in request.form.keys() for k in ["username",
                                                "password"]):
        res = check_login(request.form['username'].lower(), request.form['password'])
        if res[0] != "ok":
            response["status"] = res[0]
            return jsonify(response), 401
        
        token = create_access_token(identity=res[1].__dict__)
        response["status"] = res[0]
        response["payload"] = res[1].__dict__
        response["access_token"] = token
        return jsonify(response), 200
    else:
        response["status"] = "invalid"
        return jsonify(response), 400


@bp.route("/signup", methods = ["POST"])
def addUser():
    response = {"status": "",
                "payload": {},
                "access_token": ""}

    if all(k in request.form.keys() for k in ["username",
                                              "password",
                                              "email",
                                              ]):
        if (request.form['username'].strip() == "" or request.form['password'].strip() == "" or "@" not in request.form["email"]):
            print(request.form)
            response["status"] = "invalid"
            return jsonify(response), 400
            
        res = add_user(request.form['username'].lower(),
                       request.form['password'],
                       request.form["email"],
                       request.form["avatar"] if "avatar" in request.form.keys() else None
                       )


        if res != "ok":
            response["status"] = res
            return jsonify(response), 400
        
        else:
            response["status"] = "ok"
            return jsonify(response), 201
    else:
        response["status"] = "invalid parameters"
        return jsonify(response), 400


@bp.route("/token_test", methods=["GET"])
@jwt_required()
def token_test():
    """
    Test endpoint to check if the access token is valid
    Authorization header must be set to the access token
    :paramters:
        None
    :headers:
        Authorization: Bearer <access_token>
    :return:   json

    """
    response = {"status": "",
                "payload": {},
                }
    response["status"] = "ok"
    return jsonify(response), 200