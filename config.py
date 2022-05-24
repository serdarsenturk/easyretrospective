import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DB_CONNECTION_STRING']
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PUSHER_APP_ID = os.environ['PUSHER_APP_ID']
    PUSHER_KEY = os.environ['PUSHER_KEY']
    PUSHER_SECRET = os.environ['PUSHER_SECRET']
    PROJECT_ID = os.environ['PROJECT_ID']
    PRIVATE_KEY_ID = os.environ['PRIVATE_KEY_ID']
    PRIVATE_KEY = os.environ['PRIVATE_KEY'].replace("\\n", "\n")
    CLIENT_EMAIL = os.environ['CLIENT_EMAIL']
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_X509_CERT_URL = os.environ['CLIENT_X509_CERT_URL']
    CORS_ORIGINS = os.environ['CORS_ORIGINS']
    SENDIN_BLUE_API_KEY = os.environ['SENDIN_BLUE_API_KEY']
