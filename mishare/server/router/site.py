#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app
from mishare.lib.database import database
from flask import jsonify
from flask_login import login_required
from mishare.server.const import *

@app.route('/site_list', methods=['GET'])
@login_required
def site_list():
    sql = """
        SELECT
        `site_id`, `site_title`, `site_domain`, `site_icon`
        FROM `site`
        ORDER BY `priority`
    """

    sites = None
    with database.connection() as cur:
        cur.execute(sql)
        sites = cur.fetchall()

    return jsonify(c=CODE_OK, sites=sites)
