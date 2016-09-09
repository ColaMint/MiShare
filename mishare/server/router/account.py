#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app
from flask import jsonify
from flask_login import login_required

@app.route('/account_list/<site_id>', methods=['GET'])
@login_required
def account_list(site_id):
    pass

@app.route('/my_sharing_account_list', methods=['GET'])
@login_required
def my_sharing_account_list():
    pass

@app.route('/my_renting_account_list', methods=['GET'])
@login_required
def my_renting_account_list():
    pass

@app.route('/add_account', methods=['POST'])
@login_required
def add_account():
    pass

@app.route('/modify_account', methods=['POST'])
@login_required
def modify_account():
    pass

@app.route('/rent_account', methods=['POST'])
@login_required
def rent_account():
    pass

@app.route('/stop_renting_account', methods=['POST'])
@login_required
def stop_renting_account():
    pass

@app.route('/repoting_renting_account', methods=['POST'])
@login_required
def reporting_renting_account():
    pass
