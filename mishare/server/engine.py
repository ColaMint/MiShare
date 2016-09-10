#!/usr/bin/python
# -*- coding:utf-8 -*-


from mishare.lib.database import database
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

    def add_account(self, account_id, username, password):
        pass

    def remove_account(self, account_id, username, password):
        pass

    def get_account_status(self, account_id):
        pass

    def get_account_verification_code(self, account_id):
        pass

    def input_account_verification_code(self, account_id):
        pass

    def get_account_cookie(self, account_id):
        pass

    def validate_account(self, site_id, username, password, verification_code):
        pass

    def login_periodly(self):
        pass
