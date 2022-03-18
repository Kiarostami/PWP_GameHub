import pytest


@pytest.mark.parametrize(('url', 'message'), (
    ("/user/1", b'ok'),
    ('/user/10', b'not found'),
    ('/user/vahid', b'404 Not Found'),
    ('/user/uname/100', b'not found'),
    ('/user/uname/test2', b'ok'),
    ('/getGameList', b'ok'),
    ('/getFriends', b'ok'),
    ('/profile', b'invalid')

))
def test_get_methods(client, auth, url, message):
    auth.login()
    response = client.get(url)
    assert message in response.data


def test_profile(client, auth):
    auth.login2()
    response = client.post('/add_profile/HELLLLLLO/Invisible')
    assert b'ok' in response.data
    response = client.get("/profile")
    assert b'ok' in response.data
    response = client.post('/add_profile/HELLLLLLO/Invisible')
    assert b'invalid' in response.data
    response = client.put("/update_status/Online")
    assert b'ok' in response.data