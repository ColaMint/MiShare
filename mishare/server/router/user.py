#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app, db_required
from mishare.server.const import *
from flask import jsonify, request, g
from flask_login import login_user, logout_user

@app.route('/login_required', methods=['GET'])
def login_required():
    return jsonify(c=CODE_LOGIN_REQUIRED)

@app.route('/login', methods=['POST'])
@db_required
def login():
    pass

@app.route('/logout', methods=['POST'])
def logout():
    pass

@app.route('/register', methods=['POST'])
def register():
    pass
