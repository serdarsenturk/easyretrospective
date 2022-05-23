from marshmallow import fields
from app import ma

class CardSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    content = fields.Str()
    member_firebase_id = fields.Str()
    column_id = fields.Int()

card_schema = CardSchema()
cards_schema = CardSchema(many=True)