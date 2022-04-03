import aifc
from urllib import response
import pytest
from flask import session
from api.db import get_db
import json

@pytest.mark.parametrize(('url', 'message'), (
    ("/im/self", b'ok'),
    ('/im/others', b'ok'),
    ('/im/1', b'ok'),
    ('/im/2', b'not found')
))
def test_get_metods(client, auth, url, message):
    auth.login()
    response = client.get(url)
    assert message in response.data
def test_get_invalid_metods(client, auth):
    url = "/im/1"
    auth.login2()
    response = client.get(url)
    assert b'invalid' in response.data


@pytest.mark.parametrize(('user', 'url', 'message'), (
    (1, "/im/accmsg/1", b'invalid'),
    (1, "/im/accmsg/400", b'not found'),
    (2, '/im/accmsg/1', b'invalid'),
    (3, '/im/accmsg/1', b'ok')
))
def test_accept_msg(client, auth, user, url, message):
    if user == 1:
        auth.login()
    elif user == 2:
        auth.login2()
    else:
        auth.login3()
    response = client.put(url)
    assert message in response.data


# @pytest.mark.parametrize(('user', 'url', 'message'), (
#     
#     (2, '/im/rejmsg/1', b'invalid'),
#     (3, '/im/rejmsg/1', b'ok')
# ))
# def test_reject_msg(client, auth, user, url, message):
#     if user == 1:
#         auth.login()
#     elif user == 2:
#         auth.login2()
#     else:
#         auth.login3()
#     response = client.put(url)
#     assert message in response.data

def test_reje_msg1(client, auth):
    a = ["/im/rejmsg/1", b'invalid']
    auth.login()
    response = client.put(a[0])
    assert a[1] in response.data

def test_reje_msg2(client, auth):
    a = ["/im/rejmsg/100", b'not found']
    auth.login()
    response = client.put(a[0])
    assert a[1] in response.data

def test_reje_msg3(client, auth):
    a = ["/im/rejmsg/1", b'invalid']
    auth.login2()
    response = client.put(a[0])
    assert a[1] in response.data

def test_reje_msg4(client, auth):
    a = ["/im/rejmsg/1", b'ok']
    auth.login3()
    response = client.put(a[0])
    assert a[1] in response.data

def test_create_inv_msg(client, auth):
    auth.login()
    response = client.post("/im/crtinv/1/2/2022-02-16 12:11:24")
    assert b'ok' in response.data

@pytest.mark.parametrize(('user', 'url', 'message'), (
    (1, "/im/delinv/1", b'ok'),
    (1, "/im/delinv/400", b'not found'),
    (2, '/im/delinv/1', b'invalid'),
    (3, '/im/delinv/1', b'invalid')
))
def test_reject_msg(client, auth, user, url, message):
    if user == 1:
        auth.login()
    elif user == 2:
        auth.login2()
    else:
        auth.login3()
    response = client.delete(url)
    assert message in response.data