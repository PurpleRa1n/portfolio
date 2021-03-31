import http
from json.decoder import JSONDecodeError
from typing import Dict

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from marshmallow import ValidationError


class BaseView(web.View):
    schema_class = None

    def get_schema_class(self):
        """
        Return the class to use for the schema.
        Defaults to using `self.schema_class`.

        You may want to override this if you need to provide different
        schema depending on the incoming request.
        """
        assert self.schema_class is not None, (
                "'%s' should either include a `schema_class` attribute, "
                "or override the `get_schema_class()` method."
                % self.__class__.__name__
        )

        return self.schema_class

    async def get_payload(self) -> Dict:
        try:
            return await self.request.json()
        except JSONDecodeError:
            raise ValidationError('payload can\t be empty')

    async def get_validated_data(self, raise_exception: False):
        schema = self.get_schema_class()
        payload: Dict = await self.get_payload()
        errors = schema().validate(payload, )
        if errors:
            if raise_exception:
                raise ValidationError(errors)
            return errors
        return payload

    async def get_object_or_404(self, model, lookup):
        object = await model.get(lookup)
        if object is None:
            raise HTTPNotFound
        return object


class HealthCheckView(web.View):

    async def get(self):
        return web.json_response(data="OK", status=http.HTTPStatus.OK)
