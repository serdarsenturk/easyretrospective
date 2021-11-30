class BoardSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    member_id = fields.Int()
