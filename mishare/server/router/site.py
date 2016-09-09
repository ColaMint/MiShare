#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app, db_required
from flask import jsonify, g
from flask_login import login_required
from mishare.server.const import *
import MySQLdb

@app.route('/site_list', methods=['GET'])
@login_required
@db_required
def site_list():
    sql = """
        SELECT
        `site_id`, `site_title`, `site_url`, `site_icon`
        FROM `site`
        ORDER BY `priority`
    """

    cur = g.db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    sites = cur.fetchall()
    return jsonify(c=CODE_OK, sites=sites)
