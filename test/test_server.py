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
import simplejson as json

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


if __name__ == '__main__':
    unittest.main()
