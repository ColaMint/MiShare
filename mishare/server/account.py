#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.site.iqiyi import Iqiyi
from mishare.site.youku import Youku
from mishare.site.tencent import Tencent
from mishare.etc.config import app as app_config
from mishare.lib.database import database
from mishare.server.const import *
from mishare.site.site import *
import datetime
import threading
import random
import time
import logging


def site_id_to_site_cls(site_id):
    if site_id == SITE_ID_IQIYI:
        return Iqiyi
    elif site_id == SITE_ID_YOUKU:
        return Youku
    elif site_id == SITE_ID_TENCENT:
        return Tencent
    return None


class Account(object):
    """
    维护账号的状态
    """

    site = None
    """
    type: mishare.site.site.Site
    """

    site_id = None
    """
    网站ID
    type: int
    """

    account_id = None
    """
    账号ID
    type: int
    """

    username = None
    """
    账号
    type: string
    """

    password = None
    """
    密码
    type: string
    """

    def __init__(self,
                 site_id,
                 account_id,
                 username,
                 password):

        self.site_id = site_id
        self.account_id = account_id
        self.username = username
        self.password = password
        self.init_site()

    def init_site(self):
        site_cls = site_id_to_site_cls(self.site_id)
        self.site = site_cls(self.username, self.password)

    def input_verification_code(self, verification_code, run_async=False):
        if self.site.status == STATUS_NEED_VERIFICATION:
            self.site.input_verification_code(verification_code)

    @property
    def status(self):
        return self.site.status

    @property
    def cookies(self):
        return self.site.cookies

    @property
    def verification_code(self):
        return self.site.verification_code_png_base64


class AccountManager(object):

    accounts = None

    validating_accounts = None

    def __init__(self):
        self.accounts = {}
        self.validate_accounts = {}
        self.load_accounts()

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
            account = Account(
                site_id=site_id,
                account_id=account_id,
                username=username,
                password=password)
            logging.info(
                "account_id: %d, status: %d, cookies: %s" %
                (account.account_id, account.status, account.cookies))
            self.accounts[account_id] = account

    def remove_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]

    def pick_one_avaliable_account(self, site_id, account_id_black_list=[]):
        avaliable_accounts = []
        for account in self.accounts.values():
            print account.account_id, account.status
            if int(account.site_id) == int(site_id) \
                    and account.account_id not in account_id_black_list \
                    and account.status in [STATUS_NEED_VERIFICATION, STATUS_VALID_ACCOUNT]:
                avaliable_accounts.append(account)
        if len(avaliable_accounts) > 0:
            return random.choice(avaliable_accounts)
        else:
            return None

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

    def get_account(self, account_id):
        if account_id in self.accounts:
            return self.accounts[account_id]
        return None

    def validate_account(self, site_id, username, password, verification_code):
        key = '%d.%s.%s' % (site_id, username, password)
        account = None
        if key in self.validating_accounts:
            account = self.validate_accounts[key]
            if account.status == STATUS_NEED_VERIFICATION:
                account.input_verification_code(
                    verification_code=verification_code)
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
