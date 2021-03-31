import http
from typing import Dict

from aiohttp import web
from asyncpg import UniqueViolationError

from auth import models
from auth import schemas
from auth.constants import AuthErrors
from auth.utils import get_jwt_token
from core import views


class LoginView(views.BaseView):
    schema_class = schemas.AuthenticationSchema

    async def post(self):
        data = await self.get_validated_data(raise_exception=True)

        user = await models.User.query.where(models.User.username == data['username']).gino.first()

        if user is not None:
            password_match: bool = user.verify_password(data['password'])
        if user is None or not password_match:
            return web.json_response(
                data={'error': AuthErrors.invalid_credentials.value},
                status=http.HTTPStatus.BAD_REQUEST
            )

        jwt_token: bytes = get_jwt_token(user.id)

        return web.json_response({'token': jwt_token.decode('utf-8')})


class RegistrationView(views.BaseView):
    schema_class = schemas.AuthenticationSchema

    async def post(self):
        data: Dict = await self.get_validated_data(raise_exception=True)
        hashed_password: str = models.User.hash_password(data['password'])

        try:
            user = await models.User.create(username=data['username'], password=hashed_password)
        except UniqueViolationError:
            return web.json_response(
                data={'error': 'Username already taken'},
                status=http.HTTPStatus.BAD_REQUEST
            )

        return web.json_response(
            data={'id': user.id, 'username': data['username']},
            status=http.HTTPStatus.CREATED
        )
