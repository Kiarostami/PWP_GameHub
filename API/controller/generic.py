import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response, session
)
from werkzeug.exceptions import abort


bp = Blueprint("generic", __name__)


# Ceck user logged in or not
@bp.before_app_request
def before_req():
    whitelist = ["login", "addUser", "logout"]
    
    if 'user' not in session:
        if not any(i in request.url for i in whitelist):
            return jsonify({"status": "login required"})