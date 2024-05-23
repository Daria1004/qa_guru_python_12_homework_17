import requests
from jsonschema import validate
from schemas.user import schema_get_list_users, schema_get_single_user, schema_post_create_user, schema_put_update_user


BASE_URL = 'https://reqres.in'


def test_get_list_users():

    per_page = 7
    response = requests.get(BASE_URL + '/api/users', params={"page": 1, "per_page": per_page})

    body = response.json()

    assert response.status_code == 200

    validate(body['data'], schema_get_list_users)

    ids = []
    for user in body['data']:
        ids.append(user['id'])
    assert len(ids) == len(set(ids))

    assert len(body['data']) <= per_page


def test_get_current_user():

    response = requests.get(BASE_URL + '/api/users/1')

    assert response.status_code == 200

    body = response.json()

    validate(body['data'], schema_get_single_user)
    assert body['data']['id'] == 1
    assert body['data']['first_name'] == 'George'


def test_get_current_user_not_found():

    response = requests.get(BASE_URL + '/api/users/0')

    assert response.status_code == 404
    assert response.json() == {}


def test_post_create_user():

    payload = {
        "name": "Oleg",
        "job": "Worker"
    }

    response = requests.post(BASE_URL + '/api/users', json=payload)

    assert response.status_code == 201

    body = response.json()

    validate(body, schema_post_create_user)
    assert body['name'] == payload['name']
    assert body['job'] == payload['job']


def test_put_update_user():

    payload = {
        "name": "George2",
        "job": "Worker2"
    }

    response = requests.put(BASE_URL + '/api/users/1', json=payload)

    assert response.status_code == 200

    body = response.json()

    validate(body, schema_put_update_user)
    assert body['name'] == payload['name']
    assert body['job'] == payload['job']


def test_delete_user():

    response = requests.delete(BASE_URL + '/api/users/1')

    assert response.status_code == 204
