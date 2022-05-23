from app import app, db
from flask import Blueprint, request
from firebase_admin import auth
from flask_cors import CORS
from app.models.member import Member

member = Blueprint('member', __name__)
CORS(member, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, supports_credentials=True)

@member.route('/api/v1/member/create', methods=["POST"])
def create_member():
    id_token = request.headers['Authorization']

    try:
        decoded_claims = auth.verify_id_token(id_token)

        new_member = Member(firebase_user_id=decoded_claims['user_id'],
                            email=decoded_claims['email'], role="Member")

        db.session.add(new_member)
        db.session.commit()

        return 'Successful, a new member has created', 200
    except:
        db.session.rollback()
        return 'Failed to create a new member', 401