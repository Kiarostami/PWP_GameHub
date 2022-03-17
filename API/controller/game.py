from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort

from API.db import get_list_of_all_games

from API.models import Game

bp = Blueprint("user", __name__)


@bp.route("/gamesList", methods=['GET'])
def getGames():
    gl = get_list_of_all_games()
    return jsonify({"status": 'ok', 'payload': gl})