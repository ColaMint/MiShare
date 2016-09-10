#!/usr/bin/python
# -*- coding:utf-8 -*-

class Mishare(object):

    sau_manager = None
    """

    """

    def __init__(self):
        pass

    def is_user_using_site_account(self, user_id, site_id):
        pass

    def start_renting_account(self, user_id, site_id, verification_code=None):
        pass

    def switch_renting_account(self, user_id, site_id, verification_code=None):
        pass

    def stop_renting_account(self, user_id, site_id):
        pass

    def validate_account(self, site_id, username, password, verification_code=None):
        pass

    def add_sharing_account(self, site_id, account_id):
        pass

    def stop_sharing_account(self, site_id, account_id):
        pass
