# -*- coding: utf-8 -*-
import os
import sys
import time
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from src.models import User, News

# from flask_login import LoginManager


    # click.echo('Done.')


# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# login_manager = LoginManager(app)


# @login_manager.user_loader
# def load_user(user_id):
#     from watchlist.models import User
#     user = User.query.get(int(user_id))
#     return user


# login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'


# @app.context_processor
# def inject_user():
#     from watchlist.models import User
#     user = User.query.first()
#     return dict(user=user)

from src.models import forge, initdb

# initdb(True)
# forge()

from src import views, errors, commands