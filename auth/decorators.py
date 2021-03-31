from http import HTTPStatus
from typing import Callable, Any

from aiohttp import web

from auth.constants import AuthErrors


def login_required(func: Callable):
    """
    The decorator restricts access to the resource if the user is not logged in.
    """
    async def wrapper(view: Any):
        if not view.request.user:
            return web.json_response({'error': AuthErrors.auth_required.value}, status=HTTPStatus.UNAUTHORIZED)
        return await func(view)

    return wrapper
