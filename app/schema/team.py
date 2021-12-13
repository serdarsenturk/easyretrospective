from marshmallow import fields
from app import ma
from app.schema.board import BoardSchema

class TeamSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    columns = fields.Nested(BoardSchema, many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)