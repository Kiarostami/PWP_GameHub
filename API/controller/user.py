from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response
)
from werkzeug.exceptions import abort

from API.db import check_login
from API.db import add_user
from API.db import add_profile
from API.db import get_list_of_games

bp = Blueprint("user", __name__)


@bp.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        if all(k in request.form.keys() for k in ["username",
                                                  "password"]):
            res = check_login(request.form['username'], request.form['password'])
            # TODO: create session
            if res != "OK":
                return jsonify({"status": res})
            return jsonify({"status": "OK"})

    return jsonify({'status': 'invalid'})


@bp.route("/addUser", methods = ["POST"])
def addUser():
    if all(k in request.form.keys() for k in ["username",
                                              "password",
                                              "email",
                                              ]):
        res = add_user(request.form['username'],
                       request.form['password'],
                       request.form["email"],
                       request.form["avatar"] if "avatar" in request.form.keys() else None
                       )

        # TODO: create session
        if res != "OK":
            return jsonify({"status": res})
        return jsonify({"status": "OK"})

    return jsonify({'status': 'invalid'})


@bp.route("/getGameList", methods=["POST"])
def getUsersGame():
    if "user_id" in request.form.keys():
        user_id = request.form['user_id']
        gl = get_list_of_games(user_id)
        return jsonify({"status": "OK", 'payload': str(gl)})
    return jsonify({'status': 'invalid'})
