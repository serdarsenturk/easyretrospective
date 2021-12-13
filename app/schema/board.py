from marshmallow import fields
from app import ma
from app.schema.column import ColumnSchema

class BoardSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Str()
    code = fields.Str()
    date = fields.DateTime()
    member_id = fields.Int()
    team_id = fields.Int()
    columns = fields.Nested(ColumnSchema, many=True)

board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)