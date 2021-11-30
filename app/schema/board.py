from marshmallow import fields
from app import ma

class BoardSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    member_id = fields.Int()

board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)