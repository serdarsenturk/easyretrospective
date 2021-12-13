from marshmallow import fields
from app import ma

class ColumnUpdatedSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()

column_updated_schema = ColumnUpdatedSchema()