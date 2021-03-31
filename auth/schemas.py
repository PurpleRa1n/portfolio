import marshmallow
from marshmallow import validate


class AuthenticationSchema(marshmallow.Schema):
    username = marshmallow.fields.Str(
        required=True,
        validate=validate.Length(min=4, max=30),
    )
    password = marshmallow.fields.Str(
        required=True,
        validate=validate.Length(min=4, max=30)
    )
