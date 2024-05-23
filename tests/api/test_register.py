import requests
from jsonschema import validate
from schemas.register import schema_post_register_successful, schema_post_register_unsuccessful
from tests.api.conftest import BASE_URL


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
