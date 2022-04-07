from marshmallow import fields
from app import ma
from app.schema.board import BoardSchema


class TeamBoardSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Str()

team_board_schema = TeamBoardSchema()
team_boards_schema = TeamBoardSchema(many=True)