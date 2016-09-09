#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app
from flask import jsonify
from flask_login import login_required

@app.route('/site_list', methods=['GET'])
@login_required
def site_list():
    pass
