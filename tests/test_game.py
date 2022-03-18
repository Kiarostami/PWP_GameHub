from urllib import response
import pytest
from flask import session
from API.db import get_db
import json

@pytest.mark.parametrize(('url', 'message'), (
    ("/games", b'ok'),
    ('/games/1', b'ok'),
    ('/games/DUMMYTEST', b'ok'),
    ('/games/100', b'not found')
))
def test_games(client, auth, url, message):
    auth.login()
    response = client.get(url)
    assert message in response.data

def test_add_game(client, auth):
    auth.login2()
    response = client.post("/games/add/1")
    assert b'ok' in response.data
    response = client.post("/games/add/1")
    assert b'already added' in response.data
