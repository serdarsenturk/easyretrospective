import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DB_CONNECTION_STRING']
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PUSHER_APP_ID = os.environ['PUSHER_APP_ID']
    PUSHER_KEY = os.environ['PUSHER_KEY']
    PUSHER_SECRET = os.environ['PUSHER_SECRET']
    CORS_ORIGINS = os.environ['CORS_ORIGINS']