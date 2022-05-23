from app import db

class Member(db.Model):
    __tablename__ = 'members'

    teams_members = db.Table('teams_members',
                    db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key=True),
                    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True)
                    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    firebase_user_id = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    boards = db.relationship('Board', backref='member', lazy=True)
    cards = db.relationship('Card', backref='card', lazy=True)
    teams = db.relationship('Team', secondary=teams_members, lazy='subquery',
        backref=db.backref('Member', lazy=True))
    role = db.Column(db.Enum("Member", "TeamMember", "TeamManager", name="Role"))
    db.UniqueConstraint(firebase_user_id)