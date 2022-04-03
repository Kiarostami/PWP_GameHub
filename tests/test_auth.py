import pytest
from flask import session
from api.db import get_db


def test_register(client, app):
    assert client.post('/addUser').status_code == 200
    response = client.post(
        '/addUser', data={'username': 'a', 'password': 'a', 'email': "my@email.com"}
    )
    assert b'ok' in response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None
    



@pytest.mark.parametrize(('username', 'password', 'email', 'message'), (
    ('', '', '',b'invalid parameters'),
    ('a', '', 'email', b'invalid parameters'),
    ("abc", "DEF", "ghi", b"invalid parameters"),
    ('test', 'test', 'djda@test.com',b'user already exist'),
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/addUser',
        data={'username': username, 'password': password, 'email': email}
    )
    print(response.data)
    assert message in response.data


def test_login(client, auth):
    assert client.post('/login').status_code == 200
    response = auth.login()
    assert response.headers['Content-Type'] == 'application/json'

    with client:
        client.get('/profile')
        assert session['id'] == 1
        assert session['user'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'wrong'),
    ('test', 'a', b'wrong'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
    
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'id' not in session
