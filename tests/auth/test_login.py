import http

import faker
from tests.constants import Urls, CREDENTIALS
from tests.validators import validate_error_msg, validate_type

from auth.constants import AuthErrors

fake = faker.Faker()


class TestLogin:

    async def test_login_with_invalid_credentials_error(self, api_client):
        payload = {
            'username': fake.pystr(min_chars=4, max_chars=30),
            'password': fake.pystr(min_chars=4, max_chars=30),
        }
        response = await api_client.post(Urls.login.value, json=payload)
        await validate_error_msg(response, AuthErrors.invalid_credentials.value)

    async def test_login_with_invalid_field_error(self, api_client):
        payload = {
            'invalid_field': fake.pystr(min_chars=4, max_chars=30),
            'password': fake.pystr(min_chars=4, max_chars=30),
        }
        response = await api_client.post(Urls.login.value, json=payload)
        assert response.status == http.HTTPStatus.BAD_REQUEST
        response_data = await response.json()
        exp_data = {
            'error': {
                'username': [
                    'Missing data for required field.'
                ],
                'invalid_field': [
                    'Unknown field.'
                ]
            },
        }
        assert exp_data == response_data

    async def test_request_with_non_existing_method_error(self, api_client):
        response = await api_client.get(Urls.login.value)
        await validate_error_msg(response, 'Method Not Allowed')

    async def test_login_user_success(self, api_client, user):
        response = await api_client.post(Urls.login.value, json=CREDENTIALS)
        assert response.status == http.HTTPStatus.OK
        response = await response.json()
        assert response['token'] == validate_type(str)
