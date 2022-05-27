from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from firebase_admin import credentials
from flask_firebase_admin import FirebaseAdmin

#Define the WSGI application object
app = Flask(__name__)
ma = Marshmallow(app)

# Configurations
app.config.from_object(Config)
cert = {
    "type": "service_account",
    "project_id": app.config.get("PROJECT_ID"),
    "private_key_id": app.config.get("PRIVATE_KEY_ID"),
    "private_key": app.config.get("PRIVATE_KEY"),
    "client_email": app.config.get("CLIENT_EMAIL"),
    "client_id": app.config.get("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": app.config.get("CLIENT_X509_CERT_URL"),
}
app.config["FIREBASE_ADMIN_CREDENTIAL"] = credentials.Certificate(cert)
app.config["FIREBASE_ADMIN_AUTHORIZATION_SCHEME"] = "JWT"
app.config["FIREBASE_ADMIN_CHECK_REVOKED"] = False  # don't check for revoked tokens
app.config["FIREBASE_ADMIN_PAYLOAD_ATTR"] = "firebase_jwt"
app.config["FIREBASE_ADMIN_RAISE_IF_APP_EXISTS"] = False

# Initialize 3rd party applications
db = SQLAlchemy(app)
migrate = Migrate(app, db)
firebase = FirebaseAdmin(app)

# Import a module / component using its blueprint handler variable (ex./url)
from app.api.home import home
from app.api.board import boards
from app.api.column import columns
from app.api.card import cards
from app.api.member import members
from app.api.team import teams

#Register blueprint(s)
app.register_blueprint(home)
app.register_blueprint(boards)
app.register_blueprint(columns)
app.register_blueprint(cards)
app.register_blueprint(members)
app.register_blueprint(teams)

db.create_all()