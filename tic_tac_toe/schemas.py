import marshmallow


class FieldSchema(marshmallow.Schema):
    board = marshmallow.fields.List(
        marshmallow.fields.List(
            marshmallow.fields.Int(), required=True,
        ),
        required=True
    )


class GameSchema(marshmallow.Schema):
    id = marshmallow.fields.Int(required=True)
    active = marshmallow.fields.Bool(required=True)
    field = marshmallow.fields.Nested(FieldSchema, required=True)
    result = marshmallow.fields.Int(required=True)


class GameMoveSchema(marshmallow.Schema):
    row = marshmallow.fields.Int(required=True)
    col = marshmallow.fields.Int(required=True)
