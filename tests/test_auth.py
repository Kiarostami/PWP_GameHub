import json
import pytest
from api.db import get_db


def test_register(client, app):
    assert client.post('/signup').status_code == 400
    response = client.post(
        '/signup', json={'username': 'a', 'password': 'a', 'email': "my@email.com"}
    )
    print(response.data)
    assert b'ok' in response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None
    



@pytest.mark.parametrize(('username', 'password', 'email', 'message'), (
    ('', '', '',b'invalid'),
    ('a', '', 'email', b'invalid'),
    ("abc", "DEF", "ghi", b"invalid"),
    ('test', 'test', 'djda@test.com',b'user already exist'),
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/signup',
        json={'username': username, 'password': password, 'email': email}
    )
    print(response.data)
    assert message in response.data or message == response.status_code


def test_login(client, auth):
    assert client.post('/login').status_code == 400
    response = auth.login()
    assert response.headers['Content-Type'] == 'application/json'
    assert b'ok' in response.data

    token = json.loads(response.data.decode())['access_token']
    
    assert client.get('/token_test', 
                headers={"Authorization": "Bearer " + token}
                ).status_code == 200
    assert client.get('/token_test',
                headers={"Authorization": "Bearer 12" + token}
                ).status_code >= 400


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'wrong'),
    ('test', 'a', b'wrong'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
