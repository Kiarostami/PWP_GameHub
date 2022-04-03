import os
import tempfile

import pytest
from api import create_app
from api.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='1234'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )
    
    def login2(self, username='test2', password='1234'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def login3(self, username='test3', password='1234'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')
    

    def get_user_info(self, username):
        return self._client.get("/user/uname/"+username)


@pytest.fixture
def auth(client) -> AuthActions:
    return AuthActions(client)
