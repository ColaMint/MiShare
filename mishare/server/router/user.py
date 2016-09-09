#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app, db_required, User
from mishare.server.const import *
from mishare.etc.config import server
from flask import jsonify, request, g
from flask_login import login_user, logout_user
import os
import MySQLdb


@app.route('/login', methods=['POST'])
@db_required
def login():
    username = request.form['username']
    password = request.form['password']

    sql = """
        SELECT
        `user_id`, `nickname`, `portrait`, `contribution_value`
        FROM `user`
        WHERE
        `username` = '%s' AND `password` = '%s'""" % (username, password)

    cur = g.db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    user = cur.fetchone()

    if user:
        login_user(User(user['user_id']))
        portrait = 'http://%s%s' % (server['domain'], user['portrait'])
        return jsonify(
            c=CODE_OK,
            nickname=user['nickname'],
            portrait=portrait,
            contribution_value=user['contribution_value'])
    else:
        return jsonify(c=CODE_USER_OR_PASS_IS_WRONG)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()

@app.route('/register', methods=['POST'])
def register():
    pass
