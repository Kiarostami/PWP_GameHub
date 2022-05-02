import json


def test_accept_friend_double_side(client, auth):
    url = "/friends/"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = auth.login3()
    token3 = json.loads(response.data.decode())['access_token']
    response = client.post(url + "3", headers={"Authorization": "Bearer " + token3}, json={"user2_id": 1})
    assert response.status_code == 200

    response = client.post(url + "3", headers={"Authorization": "Bearer " + token3})
    assert response.status_code == 400
    
    # unauthorized
    response = client.post(url + "2/accept/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401

    # not found
    response = client.post(url + "1/accept/100", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404

    # accepted
    response = client.post(url + "1/accept/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200


def test_cancel_friend_request(client, auth):
    url = "/friends/"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = auth.login3()
    token3 = json.loads(response.data.decode())['access_token']

    # send a friend request
    response = client.post(url + "3", headers={"Authorization": "Bearer " + token3}, json={"user2_id": 1})
    assert response.status_code == 200
    # send a friend request
    response = client.post(url + "3", headers={"Authorization": "Bearer " + token3}, json={"user1212_id": 1})
    assert response.status_code >= 400
    # cancel the request: unauthorized
    response = client.delete(url + "3/cancel/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401
    # cancel the request: not found
    response = client.delete(url + "3/cancel/100", headers={"Authorization": "Bearer " + token3})
    assert response.status_code == 404
    # cancel the request: accepted
    response = client.delete(url + "3/cancel/1", headers={"Authorization": "Bearer " + token3})
    assert response.status_code == 200


def test_delete_from_friends(client, auth):
    url = "/friends/"
    url2 = "/user/"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = auth.login3()
    token3 = json.loads(response.data.decode())['access_token']
    response = client.post(url + "3", headers={"Authorization": "Bearer " + token3}, json={"user2_id": 1})
    assert response.status_code == 200
    # accepted
    response = client.post(url + "1", headers={"Authorization": "Bearer " + token}, json={"user2_id": 3})
    assert response.status_code == 200
    response = client.delete(url2 + "3/friends", headers={"Authorization": "Bearer " + token}, json={"user2_id": 1})
    assert response.status_code == 401
    response = client.delete(url2 + "1/friends", headers={"Authorization": "Bearer " + token}, json={"userjhjhv2_id": 3})
    assert response.status_code == 400
    response = client.delete(url2 + "1/friends", headers={"Authorization": "Bearer " + token}, json={"user2_id": 3})
    assert response.status_code == 200
    response = client.delete(url2 + "3/friends", headers={"Authorization": "Bearer " + token3}, json={"user2_id": 1})
    assert response.status_code == 404
    

def test_reject_from_friends(client, auth):
    url = "/friends/"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = auth.login3()
    token3 = json.loads(response.data.decode())['access_token']
    response = client.post(url + "3", headers={"Authorization": "Bearer " + token3}, json={"user2_id": 1})
    assert response.status_code == 200

    response = client.delete(url + "3/reject/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401
    response = client.delete(url + "1/reject/3", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404
    response = client.delete(url + "1/reject/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200


def test_add_friend_double_side(client, auth):
    url = "/friends/"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = client.get(url + "1/pending", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404
    response = client.get(url + "2/pending", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401
    response = auth.login2()
    token2 = json.loads(response.data.decode())['access_token']
    response = client.post(url + "1", headers={"Authorization": "Bearer " + token2}, json={"user2_id": 2})
    assert response.status_code == 401
    response = client.get(url + "2/sent", headers={"Authorization": "Bearer " + token2})
    assert response.status_code == 404
    response = client.get(url + "2000/sent", headers={"Authorization": "Bearer " + token2})
    assert response.status_code == 401
    response = client.post(url + "2", headers={"Authorization": "Bearer " + token2}, json={"user2_id": 1})
    assert response.status_code == 200
    response = client.get(url + "1/pending", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    response = client.post(url + "2", headers={"Authorization": "Bearer " + token2}, json={"user2_id": 1})
    assert response.status_code == 200
    response = client.get(url + "2/sent", headers={"Authorization": "Bearer " + token2})
    assert response.status_code == 200
    response = client.post(url + "1", headers={"Authorization": "Bearer " + token}, json={"user2_id": 2})
    assert response.status_code == 200
    response = client.post(url + "1", headers={"Authorization": "Bearer " + token}, json={"user2_id": 100})
    assert response.status_code == 404
    response = client.post(url + "2", headers={"Authorization": "Bearer " + token2}, json={"user2_id": 1})
    assert response.status_code == 200
    response = client.get("/user/1/friends", headers={"Authorization": "Bearer " + token})




# def test_cancel_friend_request(client, auth):
#     url = "/friends/"
#     response = auth.login()
#     token = json.loads(response.data.decode())['access_token']
#     response = auth.login2()
#     token2 = json.loads(response.data.decode())['access_token']

#     # user 2 sent a friend request to user 1
#     response = client.post(url + "2/1", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 401
    
#     response = client.get(url + "2/sent", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 404
#     response = client.get(url + "2000/sent", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 401
#     response = client.post(url + "2/1", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 200
#     response = client.get(url + "1/pending", headers={"Authorization": "Bearer " + token})
#     assert response.status_code == 200
#     response = client.post(url + "2/1", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 200
#     response = client.get(url + "2/sent", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 200
#     response = client.post(url + "1/2", headers={"Authorization": "Bearer " + token})
#     assert response.status_code == 200
#     response = client.post(url + "1/200", headers={"Authorization": "Bearer " + token})
#     assert response.status_code == 404
#     response = client.post(url + "2/1", headers={"Authorization": "Bearer " + token2})
#     assert response.status_code == 200
#     response = client.get("/user/1/friends", headers={"Authorization": "Bearer " + token})

