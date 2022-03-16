from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from API.db import check_login
from API.db import add_user
from API.db import add_profile
from API.db import get_list_of_games
from API.models import User

bp = Blueprint("user", __name__)


@bp.route("/getGameList", methods=["POST"])
def getUsersGame():
    if "user_id" in request.form.keys():
        user_id = request.form['user_id']
        gl = get_list_of_games(user_id)
        return jsonify({"status": "OK", 'payload': str(gl)})
    return jsonify({'status': 'invalid'})
