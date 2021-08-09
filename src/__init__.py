# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager


from src import views, errors, commands


cursor.execute("DROP TABLE IF EXISTS SINA ")

# Create table as per requirement
sql = """CREATE TABLE SINA (
 TITLE CHAR(50),
 DATE CHAR(20),
 SOURCE CHAR(50),
 URL CHAR(100),
 CONTENT CHAR(50)
 )"""

cursor.execute(sql)


# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'test.db'))
db_name = 'test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print(df)
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


