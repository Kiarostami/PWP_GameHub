from flask import (
    Blueprint, request, jsonify, session
)


bp = Blueprint("generic", __name__)


# Ceck user logged in or not
@bp.before_app_request
def before_req():
    whitelist = ["login", "addUser", "logout", 'hello']

    if 'user' not in session: # pragma: no cover
        if not any(i in request.url for i in whitelist):
            return jsonify({"status": "login required"})

@bp.after_app_request
def after_req(response):
    # pragma: no cover
    return response