import aifc
from urllib import response
import pytest
from flask import session
from api.db import get_db
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

    # # invalid suggestedTime
    # response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 1, "suggestedTime": "2022-02-16 12:11:24:00"})
    # assert response.status_code == 400

    # accepted
    response = client.post(url + "/1", headers={"Authorization": "Bearer " + token}, json={"receiver_id": 2, "game_id": 1, "suggestedTime": "2022-02-16 12:11:24"})
    assert response.status_code == 201

    response = client.get(url + "/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200

