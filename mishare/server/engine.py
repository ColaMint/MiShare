#!/usr/bin/python
# -*- coding:utf-8 -*-


from mishare.lib.database import database
from mishare.server.account import Account
from mishare.site.site import *
from mishare.etc.config import app as app_config
import datetime
import MySQLdb
import threading
import time


class Engine(object):

    accounts = None

    validating_accounts = None

    def __init__(self):
        self.accounts = {}
        self.validate_accounts = {}

    def load_accounts(self):
        with database.connection() as cur:
            sql = """
                SELECT
                `account_id`,
                `user_id`,
                `site_id`,
                `username`,
                `password`,
                `max_concurrency_user`
                FROM
                `account`
                WHERE
                `status` = 1
                AND `vip_end_date` > '%s'""" % (datetime.datetime.now().strftime('%Y-%m-%d'),)
            cur.execute(sql)
            accounts = cur.fetchall()
            for account in accounts:
                self.add_account(
                    site_id=account['site_id'],
                    account_id=account['account_id'],
                    username=account['username'],
                    password=account['password'])

    def add_account(self, site_id, account_id, username, password):
        if account_id not in self.accounts:
            self.accounts[
                account_id] = Account(
                site_id=site_id,
                account_id=account_id,
                username=username,
                password=password)

    def remove_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]

    def get_account_status(self, account_id):
        if account_id in self.accounts:
            return self.accounts[account_id].status
        return None

    def get_verification_code(self, account_id):
        if account_id in self.accounts:
            return self.accounts[account_id].verification_code
        return None

    def input_verification_code(self, account_id):
        if account_id in self.accounts:
            self.accounts[account_id].input_verification_code(run_async=False)
            return self.accounts[account_id]
        return None

    def get_account_cookies(self, account_id):
        if account_id in self.accounts:
            return self.accounts[account_id].cookies
        return None

    def validate_account(self, site_id, username, password, verification_code):
        key = '%d.%s.%s' % (site_id, username, password)
        account = None
        if key in self.validating_accounts:
            account = self.validate_accounts[key]
            if account.status == STATUS_NEED_VERIFICATION:
                account.input_verification_code(verification_code=verification_code)
            else:
                account.username = username
                account.password = password
                account.login(run_async=False)
        else:
            account = Account(
                site_id=site_id,
                account_id=None,
                username=username,
                password=password)
            self.validating_accounts[key] = account
            account.login()
        return account

    def login_periodly(self, run_async=False):
        if run_async:
            t = threading.Thread(target=self.login, args=(True))
            t.daemon = False
            t.start()
        else:
            self.settle(True)

    def login(self):
        while(True):
            for account_id, account in self.accounts.iteritems():
                if account.status == STATUS_NO_LOGIN or STATUS_VALID_ACCOUNT:
                    account.login(run_async=True)
                elif account.status == STATUS_NEED_VERIFICATION:
                    continue
                elif account.status ==  STATUS_USERNAME_OR_PASSWORD_ERROR or STATUS_INVALID_ACCOUNT:
                    #TODO
                    continue
