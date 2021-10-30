# Statement for enabling the development environment
DEBUG = True

import os

# Define the database - we are working with
# Postgresql for this example
SQLALCHEMY_DATABASE_URI = os.environ['DB_CONNECTION_STRING']
