import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DB_CONNECTION_STRING']
