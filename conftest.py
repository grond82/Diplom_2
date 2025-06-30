import pytest
import requests
from url import TestUrl
from data import Data

@pytest.fixture()
def get_auth_token():
    response = requests.post(TestUrl.AUTHORIZATION_USER_URL, data=Data.CREATE_USER_FULL)
    return response.json().get('accessToken')

@pytest.fixture()
def create_delete_user():
    response = requests.post(TestUrl.CREATE_USER_URL, data=Data.CREATE_USER_FULL)
    yield response.status_code, response.json()
    requests.delete(TestUrl.USER_URL, headers={'Authorization': response.json().get('accessToken')})