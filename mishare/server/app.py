#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from flask import Flask, g
from mishare.lib.database import Database
from mishare.etc.config import database
from flask_login import LoginManager, UserMixin

db = Database(
    host=database['host'],
    port=database['port'],
    user=database['user'],
    passwd=database['passwd'],
    db=database['db'])


static_folder = os.path.abspath(os.path.join(__file__, '../../static'))
app = Flask(__name__, static_folder=static_folder)
app.secret_key = 'mishare'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_required"

class User(UserMixin):

    user_id = None
    """
    用户ID
    type: int
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def db_required(func):
    def wrapper(*args, **kw):
        g.db = db.connection()
        return func(*args, **kw)
    return wrapper

@app.teardown_request
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


