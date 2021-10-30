from flask import Blueprint

home = Blueprint('home', __name__)

@home.route('/')
def homeView():
    return "<h1>Welcome to Easyretrospective TOOL.</h1>"