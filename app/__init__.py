from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

#Define the WSGI application object

app = Flask(__name__)
ma = Marshmallow(app)

# Configurations
app.config.from_object('config')
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (ex./url)
from app.api.home import home

#Register blueprint(s)
app.register_blueprint(home)
