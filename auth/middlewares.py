from http import HTTPStatus
from typing import Callable, Union

import jwt
from aiohttp import web
from aiohttp.web_request import Request

from auth.constants import AuthErrors
from auth.models import User
from core import settings


@web.middleware
async def auth_middleware(request: Request, handler: Callable):
    """
    Middleware, which checks the request header for the presence of a token and tries to get the User instance from
    the database by token.
    In case of an error, it will return 400 status code.
    """
    request.user = None
    jwt_token: Union[str, None] = request.headers.get(settings.AUTH_HEADER)

    if jwt_token is not None:
        jwt_token = jwt_token[7:] if jwt_token.startswith(settings.AUTH_TOKEN_PREFIX) else jwt_token
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return web.json_response({'error': AuthErrors.invalid_token.value}, status=HTTPStatus.BAD_REQUEST)

        request.user = await User.get(payload['user_id'])
    return await handler(request)
