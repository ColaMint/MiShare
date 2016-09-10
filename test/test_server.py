#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../../')))
import unittest
from mishare.server.app import app
from mishare.server.const import *
from mishare.server.router import account, site, user
from mishare.server.sau import SAUManager
from mishare.server.account import Account
from mishare.server.settle import Settle
from mishare.lib.database import database
from mishare.site.site import *
from mishare.etc.config import app as app_config
import simplejson as json
import time


class TestServer(unittest.TestCase):

    @property
    def client(self):
        return app.test_client()

    @property
    def login_client(self):
        client = self.client
        data = {
            'username': 'liming',
            'password': 'BC6A4E700FCA7EB9615D8FA1E111FFDF',
        }
        client.post('/login', data=data)
        return client

    def test_login(self):
        data = {
            'username': 'liming',
            'password': 'BC6A4E700FCA7EB9615D8FA1E111FFDF',
        }
        rv = self.client.post('/login', data=data)
        result = json.loads(rv.data)
        self.assertEqual(CODE_OK, result['c'])
        self.assertEqual(u'李铭', result['nickname'])
        self.assertTrue('liming.png' in result['portrait'])
        self.assertTrue('http' in result['portrait'])

        data = {
            'username': 'liming',
            'password': 'mingli',
        }
        rv = self.client.post('/login', data=data)
        result = json.loads(rv.data)
        self.assertEqual(CODE_USER_OR_PASS_IS_WRONG, result['c'])

    def test_login_required(self):
        rv = self.client.get('/site_list')
        result = json.loads(rv.data)
        self.assertEqual(CODE_LOGIN_REQUIRED, result['c'])

    def test_site_list(self):
        rv = self.login_client.get('/site_list')
        result = json.loads(rv.data)
        self.assertEqual(CODE_OK, result['c'])
        self.assertGreater(len(result['sites']), 0)

    def test_sau(self):
        sau_manager = SAUManager()
        self.assertEqual(0, len(sau_manager.query(1, 2, 3)))
        sau_manager.add(1, 2, 3)
        sau_manager.add(1, 2, 3)
        self.assertEqual(1, len(sau_manager.query(1, 2, 3)))
        sau_manager.add(2, 2, 3)
        sau_manager.add(3, 2, 3)
        sau_manager.add(4, 2, 4)
        self.assertEqual(4, len(sau_manager.query(None, 2, None)))
        self.assertEqual(3, len(sau_manager.query(None, 2, 3)))
        sau_manager.remove(4, 2, 4)
        self.assertEqual(3, len(sau_manager.query(None, 2, None)))
        self.assertEqual(3, len(sau_manager.query(None, 2, 3)))

    def test_account(self):
        account = Account(
            site_id=1,
            account_id=1,
            username='13710230105',
            password='03545328')
        account.login_if_need(run_async=False)
        self.assertIn(
            account.site.status,
            [STATUS_NEED_VERIFICATION, STATUS_VALID_ACCOUNT,
             STATUS_INVALID_ACCOUNT])
        if account.status == STATUS_NEED_VERIFICATION:
            account.input_verification_code(
                verification_code='test', run_async=False)
            self.assertEqual(account.status, STATUS_VERIFICATION_ERROR)
        elif account.status == STATUS_VALID_ACCOUNT:
            self.assertGreater(len(account.cookies), 0)

    def test_settle(self):
        def get_user_cv(user_id):
            with database.connection() as cur:
                sql = """
                SELECT
                `contribution_value`
                FROM
                `user`
                WHERE
                `user_id` = %d
                """ % user_id
                cur.execute(sql)
                return cur.fetchone()['contribution_value']

        sau_manager = SAUManager()
        sau_manager.add(1, 2, 3)
        sau_manager.add(2, 2, 4)
        settle = Settle(sau_manager=sau_manager)
        settle.add_account(5)
        settle.add_account(5)
        self.assertIsNotNone(settle.find_user_site(user_id=3, site_id=1))
        self.assertIsNotNone(settle.find_user_site(user_id=4, site_id=2))
        self.assertIsNone(settle.find_user_site(user_id=1, site_id=2))
        settle.settle(loop=False)
        cv2_1 = get_user_cv(user_id=2)
        cv3_1 = get_user_cv(user_id=3)
        cv4_1 = get_user_cv(user_id=4)
        self.assertIsNotNone(settle.find_account(account_id=2))
        self.assertIsNone(settle.find_account(account_id=3))
        time.sleep(app_config['settle_interval'])
        settle.settle(loop=False)
        settle.report_user_site(user_id=3)
        settle.report_user_site(user_id=4)
        self.assertGreater(settle.find_account(account_id=2).used_seconds)
        self.assertGreater(
            settle.find_user_site(
                user_id=3,
                site_id=1).used_seconds)
        self.assertGreater(
            settle.find_user_site(
                user_id=3,
                site_id=2).used_seconds)
        time.sleep(app_config['settle_interval'])
        settle.settle(loop=False)
        settle.report_user_site(user_id=3)
        settle.report_user_site(user_id=4)
        cv2_2 = get_user_cv(user_id=2)
        cv3_2 = get_user_cv(user_id=3)
        cv4_2 = get_user_cv(user_id=4)
        self.assertEqual(cv2_2-cv2_1, 2*app_config['cv_per_settle_unit'])
        self.assertEqual(cv3_2-cv3_1, -app_config['cv_per_settle_unit'])
        self.assertEqual(cv4_2-cv4_1, -app_config['cv_per_settle_unit'])

        sau_manager = SAUManager()
        sau_manager.add(1, 2, 3)
        settle.add_user_site(user_id=3, site_id=1)
        settle.add_account(account_id=2)
        time.sleep(2*app_config['settle_interval'])
        settle.settle(loop=False)
        self.assertIsNone(settle.find_user_site(user_id=3, site_id=1))
        self.assertIsNotNone(settle.find_account(account_id=2))

if __name__ == '__main__':
    unittest.main()
