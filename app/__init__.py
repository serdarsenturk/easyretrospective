from flask import Flask
#Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Import a module / component using its blueprint handler variable (ex./url)
from app.api.home import home

#Register blueprint(s)
app.register_blueprint(home)
