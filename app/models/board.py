from app import db


class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    code = db.Column(db.String(8), nullable=False, unique=True, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)