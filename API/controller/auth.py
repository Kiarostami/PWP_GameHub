from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from API.db import check_login
from API.db import add_user
from API.models import User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        if all(k in request.form.keys() for k in ["username",
                                                  "password"]):
            res = check_login(request.form['username'], request.form['password'])
            if res[0] != "OK":
                return jsonify({"status": res})
            session.clear()
            session['user'] = res[1].username
            session['id'] = res[1].id
            return jsonify({"status": "OK"})

    return jsonify({'status': 'invalid'})


@bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return jsonify({"status": "OK"})


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


        if res != "OK":
            return jsonify({"status": res})
        
        return jsonify({"status": "OK"})

    return jsonify({'status': 'invalid'})