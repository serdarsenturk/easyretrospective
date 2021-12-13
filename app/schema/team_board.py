from marshmallow import fields
from app import ma

class TeamBoardSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Str()
    code = fields.Str()
    date = fields.DateTime()

team_board_schema = TeamBoardSchema()
team_boards_schema = TeamBoardSchema(many=True)