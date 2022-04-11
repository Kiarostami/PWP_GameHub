import pytest
import json

@pytest.mark.parametrize(('url', 'message'), (
    ('/games/1', b'ok'),
    ('/games/DUMMYTEST', b'ok'),
    ('/games/100', b'not found')
))
def test_games(client, auth, url, message):
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = client.get(url, headers={"Authorization": "Bearer " + token})
    assert message in response.data
