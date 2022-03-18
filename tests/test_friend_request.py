import pytest
from flask import session
from API.db import get_db
import json


@pytest.mark.parametrize(('url', 'message'), (
    ("/fr/sent", b'login'),
    ('/fr/received', b'login')
))
def test_get_methods_before_login(client, app, url, message):
    response = client.get(url)
    assert message in response.data


@pytest.mark.parametrize(('url', 'message'), (
    ("/fr/sent", b'ok'),
    ('/fr/received', b'ok')
))
def test_get_methods(client, auth, url, message):
    auth.login()
    response = client.get(url)
    assert message in response.data


@pytest.mark.parametrize(('url', 'message'), (
    ("/fr/", b'ok'),
))
def test_add_friend(client, auth, url, message):
    auth.login()
    user_test2 = auth.get_user_info('test2')
    uid = (user_test2.json['payload'])['id']
    response = client.post(url + str(uid))
    assert message in response.data


@pytest.mark.parametrize(('url', 'message'), (
    ("/fr/", b'already sent'),
))
def test_add_friend_duplicate(client, auth, url, message):
    auth.login()
    user_test2 = auth.get_user_info('test2')
    uid = (user_test2.json['payload'])['id']
    client.post(url + str(uid))
    response = client.post(url + str(uid))
    assert message in response.data


def test_add_friend_double_side(client, auth):
    url = "/fr/"
    auth.login()
    user_test2 = auth.get_user_info('test2')
    uid = (user_test2.json['payload'])['id']
    response = client.post(url + str(uid))
    assert b'ok' in response.data
    auth.logout()
    auth.login2()
    user_test1 = auth.get_user_info('test')
    uid = (user_test1.json['payload'])['id']
    response = client.post(url + str(uid))
    assert b'accepted' in response.data
    response = client.post(url + str(uid))
    assert b'already friend' in response.data


def test_delete_friend_req(client, auth):
    url = "/fr/"
    auth.login()
    user_test2 = auth.get_user_info('test2')
    uid = (user_test2.json['payload']['id'])
    response = client.post(url + str(uid))
    assert b'ok' in response.data
    auth.logout()
    auth.login2()
    user_test1 = auth.get_user_info('test')
    uid = (user_test1.json['payload'])
    response = client.get("/fr/received")
    im = response.json['payload'][0]
    response = client.delete("/fr/" + str(im['id']))
    
    assert b'ok' in response.data

def test_accept_friend_double_side(client, auth):
    url = "/fr/"
    auth.login()
    user_test2 = auth.get_user_info('test2')
    uid = (user_test2.json['payload'])['id']
    response = client.post(url + str(uid))
    assert b'ok' in response.data
    auth.logout()
    auth.login2()
    response = client.get("/fr/received")
    im = response.json['payload'][0]
    response = client.put("/fr/" + str(im['id']))
    assert b'accepted' in response.data
    response = client.put("/fr/" + str(im['id']))
    assert b'not found' in response.data
