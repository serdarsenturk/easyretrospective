from marshmallow import fields
from app import ma
from app.schema.card import CardSchema


class ColumnSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    cards = fields.Nested(CardSchema, many=True)

column_schema = ColumnSchema()