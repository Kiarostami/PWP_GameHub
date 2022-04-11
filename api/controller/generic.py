from flask import (
    Blueprint
)


bp = Blueprint("generic", __name__)


@bp.before_app_request
def before_req():
    pass

@bp.after_app_request
def after_req(response):
    # pragma: no cover
    return response