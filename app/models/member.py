from app import db

class Member(db.Model):
    __tablename__ = 'members'
    __table_args__ = (
        db.UniqueConstraint('membership_id', 'name', 'mail', name='unq_membership_id_mail'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(15), nullable=False)
