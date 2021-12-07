from app import db

class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(15), nullable=True)
    code = db.Column(db.String(8), nullable=False, unique=True, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    columns = db.relationship('Column', backref='column', lazy=True)