import json
import pytest


@pytest.mark.parametrize(('url', 'message'), (
    ("/user/1", b'ok'),
    ('/user/10', b'not found'),
    ("/user/1/profile", b'not found'),
    ('/user/1/games', b'not found'),
    ('/user/1/friends', b'not found')

))
def test_get_methods(client, auth, url, message):
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = client.get(url, headers={"Authorization": "Bearer " + token})
    assert message in response.data


def test_profile(client, auth):
    response = auth.login2()
    token = json.loads(response.data.decode())['access_token']
    response = client.post('/user/1000/profile/HELLLLLLO/Invisible', headers={"Authorization": "Bearer " + token})
    assert b'unauthorized' in response.data
    response = client.put('/user/1000/profile/bio/Invisible', headers={"Authorization": "Bearer " + token})
    assert b'unauthorized' in response.data
    response = client.put('/user/1000/profile/status/Invisible', headers={"Authorization": "Bearer " + token})
    assert b'unauthorized' in response.data
    response = client.put('/user/2/profile/bio/Terve!', headers={"Authorization": "Bearer " + token})
    assert b'does not' in response.data
    response = client.put('/user/2/profile/status/online', headers={"Authorization": "Bearer " + token})
    assert b'does not' in response.data
    response = client.post('/user/2/profile/HELLLLLLO/Invisible', headers={"Authorization": "Bearer " + token})
    assert b'ok' in response.data
    response = client.get('/user/2/profile', headers={"Authorization": "Bearer " + token})
    assert b'ok' in response.data
    response = client.put('/user/2/profile/bio/Terve!', headers={"Authorization": "Bearer " + token})
    assert b'ok' in response.data
    response = client.put('/user/2/profile/status/online', headers={"Authorization": "Bearer " + token})
    assert b'ok' in response.data
    response = client.post('/user/2/profile/HELLLLLLO/Invisible', headers={"Authorization": "Bearer " + token})
    assert b'already' in response.data
    

def test_games(client, auth):
    response = auth.login2()
    token = json.loads(response.data.decode())['access_token']
    response = client.get('/user/2/games', headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404
    response = client.post('/user/2/games/1', headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    response = client.get('/user/2/games', headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    response = client.post('/user/2000/games/1', headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401
    response = client.post('/user/2/games/2000', headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404
    response = client.post('/user/2/games/1', headers={"Authorization": "Bearer " + token})
    assert response.status_code == 400