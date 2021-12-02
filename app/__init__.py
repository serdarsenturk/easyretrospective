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

#Define the database object which is imported
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import a module / component using its blueprint handler variable (ex./url)
from app.api.home import home
from app.api.board import boards

#Register blueprint(s)
app.register_blueprint(home)
app.register_blueprint(boards)

db.create_all()