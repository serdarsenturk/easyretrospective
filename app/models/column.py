from app import db

class Column(db.Model):
    __tablename__ = 'columns'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
    cards = db.relationship('Card', backref='cards', lazy=True)