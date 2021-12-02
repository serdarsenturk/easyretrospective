from marshmallow import fields
from app import ma

class BoardSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    code = fields.Str()

board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)