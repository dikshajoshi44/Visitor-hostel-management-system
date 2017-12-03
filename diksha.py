import flask
from flask import Flask, render_template,request
from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app=Flask(__name__)
app.config.from_object(config['dev'])

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from views import *
from models import *


if __name__=='__main__':
    app.run(debug=True)