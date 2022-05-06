from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

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

#Define the database object which is imported
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import a module / component using its blueprint handler variable (ex./url)
from app.api.home import home
from app.api.board import boards
from app.api.column import columns
from app.api.card import cards

#Register blueprint(s)
app.register_blueprint(home)
app.register_blueprint(boards)
app.register_blueprint(columns)
app.register_blueprint(cards)

db.create_all()