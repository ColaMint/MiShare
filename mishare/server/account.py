#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.site.iqiyi import Iqiyi
from mishare.site.youku import Youku
from mishare.etc.config import app as app_config
from mishare.const import *
import datetime


def site_id_to_site_cls(site_id):
    if site_id == SITE_ID_IQIYI:
        return Iqiyi
    elif site_id == SITE_ID_YOUKU:
        return Youku
    elif site_id == SITE_ID_TENCENT:
        pass
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

    next_login_time = None
    """
    下次登陆时间
    type: datetime.datetime
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
        self.next_login_time = datetime.datetime.now()
        self.init_site()

    def init_site(self):
        if self.site:
            self.site.close()
        site_cls = site_id_2_site_cls(site_id)
        self.site = site_cls(username, password)

    def login(self, run_async=False):
        self.next_login_time = datetime.datetime.now(
            ) + datetime.timedelta(seconds=app_config['login_interval'])
        if self.site:
            self.init_site()
        if run_async:
            t = threading.Thread(target=self.site.login, args=())
            t.daemon = False
            t.start()
        else:
            self.site.login()

    def login_if_need(self, run_async=False):
        if datetime.datetime.now() > self.next_login_time:
            self.login(run_async=run_async)

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
