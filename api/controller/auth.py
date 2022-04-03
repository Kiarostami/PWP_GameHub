from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from api.db import check_login
from api.db import add_user

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    if all(k in request.form.keys() for k in ["username",
                                                "password"]):
        res = check_login(request.form['username'].lower(), request.form['password'])
        if res[0] != "ok":
            return jsonify({"status": res})
        session.clear()
        session['user'] = res[1].username
        session['id'] = res[1].id
        return jsonify({"status": "ok"})
    return jsonify({'status': 'not valid parameters'})
\

@bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return jsonify({"status": "ok"})


@bp.route("/addUser", methods = ["POST"])
def addUser():
    if all(k in request.form.keys() for k in ["username",
                                              "password",
                                              "email",
                                              ]):
        if (request.form['username'].strip() == "" or request.form['password'].strip() == "" or "@" not in request.form["email"]):
            return jsonify({'status': 'invalid parameters'})
        res = add_user(request.form['username'].lower(),
                       request.form['password'],
                       request.form["email"],
                       request.form["avatar"] if "avatar" in request.form.keys() else None
                       )


        if res != "ok":
            return jsonify({"status": res})
        
        return jsonify({"status": "ok"})

    return jsonify({'status': 'invalid parameters'})