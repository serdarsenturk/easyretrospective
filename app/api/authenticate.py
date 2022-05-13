from firebase_admin import auth, exceptions
import datetime
import time
from app.models.member import Member, Role

authenticate = Blueprint('authenticate', __name__)
CORS(authenticate, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, supports_credentials=True)
@authenticate.route('/api/v1/member/login', methods=['POST'])
def session_login():
    id_token = request.headers["authorization"]

    try:
        decoded_claims = auth.verify_id_token(id_token)
        # Only process if the user signed in within the last 5 minutes.
        if time.time() - decoded_claims['auth_time'] < 5 * 60:
            expires_in = datetime.timedelta(days=5)
            expires = datetime.datetime.now() + expires_in
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            response = jsonify({'status': 'success'})
            response.set_cookie(
                'session', session_cookie, expires=expires, httponly=True, secure=False)
            return response, 200
        return 'Recent sign in required', 201
    except auth.InvalidIdTokenError:
        return 'Invalid ID token', 401
    except exceptions.FirebaseError:
        return 'Failed to create a session cookie'

@authenticate.route('/api/v1/member/logout', methods=['POST'])
def session_logout():
    response = make_response("Cookie Removed")
    response.set_cookie('session', expires=0)
    return response