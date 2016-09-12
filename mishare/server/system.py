#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.server.sau import SAUManager
from mishare.server.account import AccountManager
from mishare.site.site import *

class System(object):

    sau_manager = None
    account_manager = None

    def __init__(self):
        self.sau_manager = SAUManager()
        self.account_manager = AccountManager()

    def is_user_using_site_account(self, user_id, site_id):
        return self.get_using_site_account(user_id=user_id, site_id=site_id) is not None

    def get_using_site_account(self, user_id, site_id):
        saus = self.sau_manager.search(user_id=user_id, site_id=site_id)
        if len(saus) > 0:
            return self.account_manager.get_account(saus[0].account_id)
        return None

    def start_renting_account(self, user_id, site_id, verification_code=None):
        if verification_code is None:
            account = self.account_manager.pick_one_avaliable_account(site_id=site_id)
            if account:
                self.sau_manager.add(site_id=site_id, account_id=account.account_id, user_id=user_id)
        else:
            account = self.get_using_site_account(user_id=user_id, site_id=site_id)
            if account:
                account.input_verification_code(verification_code=verification_code)
        return account

    def switch_renting_account(self, user_id, site_id, verification_code=None):
        if verification_code is None:
            self.sau_manager.remove(user_id=user_id, site_id=site_id)
        return self.start_renting_account(user_id=user_id, site_id=site_id, verification_code=verification_code)

    def stop_renting_account(self, user_id, site_id):
        self.sau_manager.remove(user_id=user_id, site_id=site_id)

    def validate_account(self, site_id, username, password, verification_code=None):
        pass

    def add_sharing_account(self, site_id, account_id):
        pass

    def stop_sharing_account(self, site_id, account_id):
        pass
