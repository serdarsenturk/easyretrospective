from app import db

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = db.Column(db.String(120), nullable=False)
    member_firebase_id = db.Column(db.String, db.ForeignKey('members.firebase_user_id'), nullable=False)
    column_id = db.Column(db.Integer, db.ForeignKey('columns.id'), nullable=False)