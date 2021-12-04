from marshmallow import fields
from app import ma
from app.schema.column import ColumnSchema


class BoardSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    code = fields.Str()
    member_id = fields.Int()
    columns = fields.Nested(ColumnSchema, many=True)

board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)