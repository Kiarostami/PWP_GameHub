import json


def test_get_and_create(client, auth):
    url = "/invitation"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']
    response = client.get(url + "/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404

    response = client.get(url + "/2", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401

    response = client.post(url + "/2", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401

    # request body empty
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 400

    # request body not compelete
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 1})
    assert response.status_code == 400

    # invalid game_id
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 100, "suggestedTime": "2022-02-16 12:11:24"})
    assert response.status_code == 404

    # invalid receiver_id
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 100, "game_id": 1, "suggestedTime": "2022-02-16 12:11:24"})
    assert response.status_code == 404

    # accepted
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 1, "suggestedTime": "2022-02-16 12:11:24"})
    assert response.status_code == 201

    response = client.get(url + "/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200


def test_delete_invite_message(client, auth):
    url = "/invitation"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']

    # create
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 1, "suggestedTime": "2022-02-16 12:11:24"})
    assert response.status_code == 201

    # unauthorized
    response = client.delete(url + "/2/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401

    # invite msg not found
    response = client.delete(url + "/1/100", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 404

    # delete unauthorized
    response = client.delete(url + "/1/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401

    # delete
    response = client.delete(url + "/1/2", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200


def test_update_invite_message(client, auth):
    url = "/invitation"
    response = auth.login()
    token = json.loads(response.data.decode())['access_token']

    # create
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 1, "suggestedTime": "2022-02-16 12:11:24"})
    assert response.status_code == 201

    response = auth.login2()
    token2 = json.loads(response.data.decode())['access_token']

    # unauthorized
    response = client.put(url + "/2/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 401

    # not found
    response = client.put(url + "/2/100", headers={"Authorization": "Bearer " + token2})
    assert response.status_code == 404

    # invalid json body 
    response = client.put(url + "/2/1", headers={"Authorization": "Bearer " + token2})
    assert response.status_code == 400

    # invalid json body 
    response = client.put(url + "/2/1", headers={"Authorization": "Bearer " + token2}, json={"acceptedXX": True})
    assert response.status_code == 400

    # invalid accepted value
    response = client.put(url + "/2/1", headers={"Authorization": "Bearer " + token2}, json={"accepted": "no"})
    assert response.status_code == 400

    # invalid user as receiver 
    response = client.put(url + "/1/2", headers={"Authorization": "Bearer " + token}, json={"accepted": True})
    assert response.status_code == 400

    # valid update
    response = client.put(url + "/2/2", headers={"Authorization": "Bearer " + token2}, json={"accepted": True})
    print(response.data)
    assert response.status_code == 200
