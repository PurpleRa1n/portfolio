import http
import traceback
from typing import Callable, Awaitable

from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPNotFound
from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from marshmallow import ValidationError


@middleware
async def error_middleware(
        request: Request,
        handler: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        response: Response = await handler(request)
    except ValidationError as e:
        response = json_response(data={'error': e.messages}, status=http.HTTPStatus.BAD_REQUEST)
    except HTTPMethodNotAllowed:
        response = json_response(data={'error': 'Method Not Allowed'}, status=http.HTTPStatus.BAD_REQUEST)
    except HTTPNotFound:
        response = json_response(data={'error': 'Required url not founds'}, status=http.HTTPStatus.NOT_FOUND)
    except Exception:
        response = json_response(data={'error': traceback.format_exc()}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
    return response
