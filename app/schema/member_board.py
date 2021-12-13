from marshmallow import fields
from app import ma

class MemberBoardSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Str()
    code = fields.Str()
    date = fields.DateTime()

member_board_schema = MemberBoardSchema()
member_boards_schema = MemberBoardSchema(many=True)