from marshmallow import fields
from app import ma
from app.schema.card import CardSchema


class ColumnSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    column_name = fields.Str()
    board_id = fields.Int()
    cards = fields.Nested(CardSchema, many=True)

column_schema = ColumnSchema()
columns_schema = ColumnSchema(many=True)