#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from flask import jsonify, Flask, g
from mishare.lib.database import Database
from mishare.etc.config import database
from mishare.server.const import *
from flask_login import LoginManager, UserMixin
from functools import wraps

db = Database(
    host=database['host'],
    port=database['port'],
    user=database['user'],
    passwd=database['passwd'],
    db=database['db'])


static_folder = os.path.abspath(os.path.join(__file__, '../../../static'))
app = Flask(__name__, static_folder=static_folder)
app.secret_key = 'mishare'

def login_required():
    return jsonify(c=CODE_LOGIN_REQUIRED)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(login_required)

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
    @wraps(func)
    def wrapper(*args, **kw):
        g.db = db.connection()
        return func(*args, **kw)
    return wrapper

@app.teardown_request
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
