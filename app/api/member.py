from __future__ import print_function
from app import app, db
from flask import Blueprint, request
from firebase_admin import auth
from flask_cors import CORS
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from app.models.member import Member

member = Blueprint('member', __name__)
CORS(member, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, supports_credentials=True)

# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = app.config.get("SENDIN_BLUE_API_KEY")

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_greeting_mail(user_id, email):
    subject = f"{email}: Thank you for registering."
    sender = {"name": "Serdar Senturk", "email": "serdarsenturk@windowslive.com"}
    to = [{"email": email, "name": user_id}]
    cc = [{"email": "example2@example2.com", "name": "Janice Doe"}]
    bcc = [{"name": "John Doe", "email": "example@example.com"}]
    reply_to = {"email": "replyto@domain.com", "name": "John Doe"}
    headers = {"Some-Custom-Name": "unique-id-1234"}
    params = {"parameter": "My param value", "subject": "New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers,
                                                   sender=sender, subject=subject, params=params,
                                                    template_id=1)

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

@member.route('/api/v1/member/create', methods=["POST"])
def create_member():
    id_token = request.headers['Authorization']

    try:
        decoded_claims = auth.verify_id_token(id_token)
        user_id = decoded_claims['user_id']
        email = decoded_claims['email']
        new_member = Member(firebase_user_id=decoded_claims['user_id'],
                            email=decoded_claims['email'], role="Member")

        send_greeting_mail(user_id, email)
        db.session.add(new_member)
        db.session.commit()

        return 'Successful, a new member has created', 200
    except:
        db.session.rollback()
        return 'Failed to create a new member', 401