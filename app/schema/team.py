from marshmallow import fields
from app import ma

class TeamSchema(ma.SQLAlchemyAutoSchema):
        id = fields.Int()
        name = fields.Str()

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)