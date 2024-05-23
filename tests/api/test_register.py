import requests
from jsonschema import validate
from schemas.register import schema_post_register_successful, schema_post_register_unsuccessful

BASE_URL = 'https://reqres.in'


def test_post_register_successful():

    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    response = requests.post(BASE_URL + '/api/register', json=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, schema_post_register_successful)
    assert body['id'] > 0
    assert len(body['token']) == 17

    print(response.status_code)
    print(response.json())


def test_post_register_unsuccessful():

    payload = {
        "email": "george.bluth@reqres.in",
        "password": ""
    }

    response = requests.post(BASE_URL + '/api/register', json=payload)
    body = response.json()

    assert response.status_code == 400
    validate(body, schema_post_register_unsuccessful)
    assert body['error'] == 'Missing password'

    print(response.status_code)
    print(response.json())
