#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.etc.config import app as app_config
from mishare.lib.database import database
import time
import threading
import datetime

class Settle(object):

    sau_manager = None

    accounts = None

    user_sites = None

    def __init__(self, sau_manager):
        self.sau_manager = sau_manager
        self.accounts = {}
        self.user_sites = {}

    def find_account(self, account_id):
        return self.accounts.get(account_id, None)

    def find_user_site(self, user_id, site_id):
        key = '%d.%d' % (user_id, site_id)
        return self.user_sites.get(key, None)

    def settle_periodly(self, run_async=False):
        if run_async:
            t = threading.Thread(target=self.settle, args=(True))
            t.daemon = True
            t.start()
        else:
            self.settle(True)

    def settle(self, loop=True):
        while(loop):
            for site_id, account_id, user_id in self.sau_manager.search():
                if self.find_account(account_id=account_id):
                    self.settle_account(account_id=account_id)
                else:
                    self.add_account(account_id)
                if not self.find_user_site(user_id=user_id, site_id=site_id):
                    self.add_user_site(user_id=user_id, site_id=site_id)
            self.clear_user_site()
            if loop:
                time.sleep(app_config['settle_interval'])

    def settle_account(self, account_id):
        account = self.find_account[account_id]
        if account is None:
            return
        now = datetime.datetime.now()
        delta_seconds = (now - account.last_settle_time).seconds
        account.used_seconds += delta_seconds
        units = account.used_seconds / app_config['cv_settle_unit_seconds']
        if units > 0:
            account.used_seconds -= units * 3600
            cv = units * app_config['cv_per_settle_unit']
            self.modify_user_contribution_value(user_id=account.owner_user_id, cv_diff=cv)
        account.last_settle_time = now

    def settle_user_site(self, user_id, site_id):
        user_site = self.find_user_site(user_id=user_id, site_id=site_id)
        if user_site is None:
            return
        now = datetime.datetime.now()
        delta_seconds = (now - user_site.last_report_time).seconds
        user_site.used_seconds += delta_seconds
        units = user_site.used_seconds / app_config['cv_settle_unit_seconds']
        if units > 0:
            user_site.used_seconds -= units * 3600
            cv = units * app_config['cv_per_settle_unit']
            self.modify_user_contribution_value(user_id=user_id, cv_diff=-cv)

        user_site.last_report_time = now

    def add_account(self, account_id):
        if account_id not in self.accounts:
            self.accounts[account_id] = Account(account_id=account_id)

    def add_user_site(self,user_id, site_id):
        user_site = self.find_user_site(user_id=user_id, site_id=site_id)
        if user_site is not None:
            return
        user_site = UserSite(user_id=user_id, site_id=site_id)
        key = '%d.%d' % (user_id, site_id)
        self.user_sites[key] = user_site
        self.modify_user_contribution_value(user_id=-user_id, cv_diff=-app_config['cv_per_settle_unit'])

    def clear_user_site(self):
        now = datetime.datetime.now()
        for key, user_site in self.user_sites.iteritems():
            if (now - user_site.last_report_time) >= datetime.timedelta(seconds=2*app_config['settle_interval']):
                del self.user_sites[key]
                self.sau_manager.remove(user_id=user_id, site_id=site_id)

    def report_user_site(self, user_id, site_id, in_use):
        if in_use:
            self.settle_user_site(user_id=user_id, site_id=site_id)

    def modify_user_contribution_value(self, user_id, cv_diff):
        with database.connection() as cur:
            sql = """
                UPDATE
                `user`
                SET
                `contribution_value` = `contribution_value` + %d
                WHERE
                `user_id` = %d""" % (-cv_diff, user_id)
            cur.execute(sql)


class Account(object):

    account_id = None

    owner_user_id = None

    used_seconds = None

    last_settle_time = None

    def __init__(self, account_id):
        self.account_id = account_id
        self.used_seconds = 0
        self.last_settle_time = datetime.datetime.now()
        self._get_owner_user_id()

    def _get_owner_user_id(self):
        with database.connection() as cur:
            sql = """
                SELECT
                `user_id`
                FROM
                `account`
                WHERE
                `account_id` = %d
            """ % self.account_id
            cur.execute(sql)
            self.owner_user_id = cur.fetchone()['user_id']

class UserSite(object):

    user_id = None

    site_id = None

    used_seconds = None

    last_report_time = None

    def __init__(self, user_id, site_id):
        self.user_id = user_id
        self.site_id = site_id
        self.used_seconds = 0
        self.last_report_time = datetime.datetime.now()
