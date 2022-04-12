import json
import pytest

@pytest.mark.parametrize(('url', 'message'), (
    ('/genres/1', b'ok'),
    ('/genres/100', b'not found'),
))
def test_genres(client, auth, url, message):
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = client.get(url, headers={"Authorization": "Bearer " + token})
    print(response.data)
    assert message in response.data
