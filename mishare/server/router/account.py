#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.app import app
from mishare.lib.database import database
from mishare.server.const import *
from mishare.site.site import *
from mishare.server.app import system
from mishare.etc.config import app as app_config
from mishare.etc.config import server
from flask import jsonify, request
from flask_login import login_required, current_user

@app.route('/get_contribution_value', methods=['GET'])
@login_required
def get_contribution_value():
    with database.connection() as cur:
        sql = """
            SELECT
            `contribution_value`
            FROM
            `user`
            WHERE
            `user_id` > %d""" % current_user.user_id
        cur.execute(sql)
        user = cur.fetchone()
        return jsonify(c=CODE_OK, contribution_value=user['contribution_value'])

@app.route('/my_sharing_account_list', methods=['GET'])
@login_required
def my_sharing_account_list():
    with database.connection() as cur:
        sql = """
        SELECT
        `account`.`account_id` `account_id`,
        `account`.`username` `account_username`,
        `account`.`vip_end_date` `vip_end_date`,
        `account`.`max_concurrency_user` `max_concurrency_user`,
        `account`.`status` `status`,
        `site`.`site_id` `site_id`,
        `site`.`site_title` `site_title`,
        `site`.`site_icon` `site_icon`,
        `site`.`site_domain` `site_domain`
        FROM
        `account`, `site`
        WHERE
        `account`.`user_id` = %d
        AND `account`.`site_id` = `site`.`site_id`
        """ % current_user.user_id
        cur.execute(sql)
        rows = cur.fetchall()
        accounts = []
        for r in rows:
            accounts.append({
                'account_id': r['account_id'],
                'account_username': r['account_username'],
                'site_id': r['site_id'],
                'site_icon': 'http://%s%s' % (server['domain'], r['site_icon']),
                'site_title': r['site_title'],
                'site_domain': r['site_domain'],
                'max_concurrency_user': r['max_concurrency_user'],
                'cur_concurrency_user': len(system.sau_manager.search(account_id=r['account_id'])),
                'status': r['status'],
            })
        return jsonify(c=CODE_OK, accounts=accounts)

@app.route('/my_renting_account_list', methods=['GET'])
@login_required
def my_renting_account_list():
    saus = system.sau_manager.search(user_id=current_user.user_id)
    accounts = []
    for sau in saus:
        account = {}
        with database.connection() as cur:
            sql = """
            SELECT
            `account`.`account_id` `account_id`,
            `site`.`site_id` `site_id`,
            `site`.`site_title` `site_title`,
            `site`.`site_icon` `site_icon`,
            `site`.`site_domain` `site_domain`
            FROM
            `account`, `site`
            WHERE
            `account`.`account_id` = %d
            AND `account`.`site_id` = `site`.`site_id`
            """ % sau.account_id
            cur.execute(sql)
            row = cur.fetchone()
            account['account_id']  = row['account_id']
            account['site_id']     = row['site_id']
            account['site_title']  = row['site_title']
            account['site_icon']   = 'http://%s%s' % (server['domain'], row['site_icon'])
            account['site_domain'] = row['site_domain']
        account['report_interval'] = app_config['report_interval']
        account['left_minuts'] = 59,
        account['cookies'] = system.account_manager.get_account(account_id=sau.account_id).cookies
        accounts.append(account)
    return jsonify(c=CODE_OK, accounts=accounts)

@app.route('/add_account', methods=['POST'])
@login_required
def add_account():
    pass

@app.route('/modify_account', methods=['POST'])
@login_required
def modify_account():
    pass

@app.route('/start_renting_account', methods=['POST'])
@login_required
def start_renting_account():
    user_id = current_user.user_id
    site_id = request.form['site_id']
    verification_code = request.form.get('verification_code', None)

    account = system.start_renting_account(user_id=user_id, site_id=site_id, verification_code=verification_code)

    if account is None:
        return jsonify(c=CODE_NO_AVALIABLE_ACCOUNT)
    elif account.status == STATUS_VALID_ACCOUNT:
        return jsonify(c=CODE_OK, report_interval=app_config['report_interval'], cookies=account.cookies)
    elif account.status == STATUS_NEED_VERIFICATION:
        return jsonify(c=CODE_NEED_VERIFICATION_CODE, verification_code=account.verification_code)
    else:
        return jsonify(c=CODE_NO_AVALIABLE_ACCOUNT)

@app.route('/switch_renting_account', methods=['POST'])
@login_required
def switch_renting_account():
    user_id = current_user.user_id
    site_id = request.form['site_id']
    verification_code = request.form.get('verification_code', None)

    account = system.switch_renting_account(user_id=user_id, site_id=site_id, verification_code=verification_code)

    if account is None:
        return jsonify(c=CODE_NO_AVALIABLE_ACCOUNT)
    elif account.status == STATUS_VALID_ACCOUNT:
        return jsonify(c=STATUS_VALID_ACCOUNT, report_interval=app_config['report_interval'], cookies=account.cookies)
    elif account.status == STATUS_NEED_VERIFICATION:
        return jsonify(c=CODE_NEED_VERIFICATION_CODE, verification_code=account.verification_code)
    else:
        return jsonify(c=CODE_NO_AVALIABLE_ACCOUNT)

@app.route('/stop_renting_account', methods=['POST'])
@login_required
def stop_renting_account():
    site_id = request.form['site_id']
    system.stop_renting_account(user_id=current_user.user_id, site_id=site_id)
    return jsonify(c=CODE_OK)

@app.route('/repoting_renting_account', methods=['POST'])
@login_required
def reporting_renting_account():
    pass
