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


class GameLogSchema(marshmallow.Schema):
    created_at = marshmallow.fields.DateTime(required=True)
    field = marshmallow.fields.Nested(FieldSchema, required=True)


class UserGameStats(marshmallow.Schema):
    result = marshmallow.fields.Str(required=True)
    score = marshmallow.fields.Int(required=True)
