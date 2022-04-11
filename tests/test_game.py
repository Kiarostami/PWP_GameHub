import json
import pytest

@pytest.mark.parametrize(('url', 'message'), (
    ('/games/1', b'ok'),
    ('/games/DUMMYTEST', b'DUMMYTEST'),
    ('/games/DUMMYTEST12121', b'not found'),
    ('/games/100', b'not found'),
    ('/games', b'ok')
))
def test_games(client, auth, url, message):
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = client.get(url, headers={"Authorization": "Bearer " + token})
    print(response.data)
    assert message in response.data
