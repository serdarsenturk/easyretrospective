from app import db
from flask import request
from functools import wraps
from firebase_admin import auth
from app.models.member import Member


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return 'A valid token is missing!', 401

        try:
            decoded_claims = auth.verify_id_token(token)
            requester_id = decoded_claims['user_id']
            current_user = db.session.query(Member).filter(Member.firebase_user_id == requester_id).first()
        except:
            return 'Invalid token!', 401

        return f(decoded_claims, requester_id, current_user, *args, **kwargs)

    return decorator
