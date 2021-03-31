from http import HTTPStatus

import faker

from auth.models import User
from core.database.orm import db
from tests import constants
from tests.validators import validate_type

fake = faker.Faker()


class TestRegistration:

    async def test_registration_create_user_success(self, api_client):
        payload = {
            'username': fake.pystr(min_chars=4, max_chars=30),
            'password': fake.pystr(min_chars=30, max_chars=30)
        }
        count = await db.func.count(User.id).gino.scalar()
        assert count == 0
        response = await api_client.post(constants.Urls.registration.value, json=payload)
        assert response.status == HTTPStatus.CREATED
        response_data = await response.json()
        exp_data = {
            'id': validate_type(int),
            'username': payload['username']
        }
        assert exp_data == response_data

        count = await db.func.count(User.id).gino.scalar()
        assert count == 1
        user = await User.get(response_data['id'])
        assert user.username == payload['username']
        assert user.password != payload['password']
