import os

from flask import Flask


from API.controller import generic
from API.controller import user
from API.controller import game
from API.controller import auth
from API.controller import invite_message
from API.controller import freind_request

from API import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    db.init_app(app)


    app.register_blueprint(user.bp)
    app.add_url_rule("/", endpoint="user")


    app.register_blueprint(game.bp)
    app.add_url_rule("/", endpoint="game")


    app.register_blueprint(auth.bp)
    app.add_url_rule("/", endpoint="auth")


    app.register_blueprint(invite_message.bp)
    app.add_url_rule("/", endpoint="invite_message")


    app.register_blueprint(freind_request.bp)
    app.add_url_rule("/", endpoint="friend_request")


    app.register_blueprint(generic.bp)
    app.add_url_rule("/", endpoint="generic")


    return app
