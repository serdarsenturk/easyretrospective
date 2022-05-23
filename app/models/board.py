from app import db

class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(15), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    code = db.Column(db.String(8), nullable=False, unique=True, index=True)
    member_firebase_id = db.Column(db.String, db.ForeignKey('members.firebase_user_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    columns = db.relationship('Column', backref='column', lazy=True)