#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from flask import jsonify, Flask
from mishare.server.const import *
from mishare.server.system import System
from mishare.etc.config import server
from flask_login import LoginManager, UserMixin
import logging

logging.basicConfig(filename=server['log_file'],level=server['log_level'])
logging.info('start')

static_folder = os.path.abspath(os.path.join(__file__, '../../../static'))
app = Flask(__name__, static_folder=static_folder)
app.secret_key = 'mishare'

system = System()

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

@login_manager.request_loader
def load_user_from_request(request):
    return User(2)
