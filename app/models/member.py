from app import db

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    boards = db.relationship('Board', backref='member', lazy=True)