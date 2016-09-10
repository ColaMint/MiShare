#!/usr/bin/python
# -*- coding:utf-8 -*-

from mishare.site import site
from mishare.site.iqiyi import Iqiyi
from mishare.site.youku import Youku
from mishare.lib.database import db
from mishare.etc.config import app as app_config
import datetime
import MySQLdb
import threading
import random
import time

site_id_2_site_cls = {
    1: Iqiyi,
    2: Youku,
}

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

    owner_user_id = None
    """
    账号拥有者ID
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

    max_concurrency_user = None
    """
    最大同时使用人数
    type: int
    """

    users = None
    """
    当前使用的用户
    type: set
    """

    next_login_time = None
    """
    下次登陆时间
    type: datetime.datetime
    """

    used_seconds = None
    """
    自上次结算，累计每使用的时长
    """

    last_settle_time = None
    """
    上次结算时间
    type: datetime.datetime
    """

    def __init__(self,
                 site_id,
                 account_id,
                 owner_user_id,
                 username,
                 password,
                 max_concurrency_user):

        self.site = site_id_2_site_cls[site_id](username, password)
        self.site_id = site_id
        self.account_id = account_id
        self.owner_user_id = owner_user_id
        self.username = username
        self.password = password
        self.max_concurrency_user = max_concurrency_user
        self.users = []
        self.next_login_time = None
        self.used_seconds = None
        self.last_settle_time = datetime.datetime.now()

    def login(self, run_async=False):
        if run_async:
            t = threading.Thread(target=self.site.login, args=())
            t.daemon = False
            t.start()
        else:
            self.site.login()

    def input_verification_code(self, verification_code, run_async=False):
        if run_async:
            t = threading.Thread(
                target=self.site.input_verification_code, args=(
                    verification_code,))
            t.daemon = False
            t.start()
        else:
            self.site.input_verification_code(verification_code)

    def add_user(self, user_id):
        self.users.add(user_id)

    def remove_user(self, user_id):
        self.user.remove(user_id)

    def reach_max_concurrency_user(self):
        return len(self.users) > self.max_concurrency_user

    def settle(self):
        """
        给账号拥有者结算贡献值
        """
        now = datetime.datetime.now()
        if len(self.users) > 0:
            delta_seconds = (now - self.last_settle_time).seconds
            self.used_seconds += delta_seconds
            units = self.used_seconds / app_config['cv_settle_unit_seconds']
            if units > 0:
                self.used_seconds -= units * 3600
                # 增加积分
                cv = units * app_config['cv_per_settle_unit']
                conn = db.connection()
                cur = conn.cursor(MySQLdb.cursors.DictCursor)
                sql = """
                    UPDATE
                    `user`
                    SET
                    `contribution_value` = `contribution_value` + %d
                    WHERE
                    `user_id` = %d
                """ % (cv, self.owner_user_id)
                cur.execute(sql)
                cur.commit()
                cur.close()
                conn.close()

        self.last_settle_time = now


class AccountManager(object):

    accounts = None

    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id):
        return self.accounts.get(account_id, None)

    def remove_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]

    def get_accounts(self):
        return self.accounts.values()


class SiteAccountManager(object):
    """
    管理网站与账号
    """

    site_accounts = None

    def __init__(self):
        self.site_accounts = {}

    def add_account(self, account):
        if account.site_id not in self.site_accounts:
            self.site_accounts[account.site_id] = {}
        self.site_accounts[account.site_id][account.account_id] = account

    def remove_account(self, account):
        if account.site_id not in self.site_accounts:
            return
        del self.site_accounts[account.site_id][account.account_id]

    def get_accounts(self, site_id):
        if site_id not in self.site_accounts:
            return []
        else:
            return self.site_accounts[site_id].values()


class UserSite(object):
    """
    用户与网站
    """

    user_id = None

    site_id = None

    account_id = None

    account = None

    last_eporting_time = None


    used_seconds = None

    def __init__(self, user_id, site_id, account):
        self.user_id = user_id
        self.site_id = site_id
        self.account_id = account.account_id
        self.account = account
        self.last_reporting_time = datetime.datetime.now()
        self.used_seconds = 0

    def cost_contribution_value(self, cv):
        conn = db.connection()
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            UPDATE
            `user`
            SET
            `contribution_value` = `contribution_value` + %d
            WHERE
            `user_id` = '%s'""" % (-cv, self.user_id)
        cur.execute(sql)
        cur.commit()
        cur.close()
        conn.close()


    def settle_first(self):
        """
        开始使用网站账号，马上扣除一个小时的贡献值
        """
        self.cost_contribution_value(app_config['cv_per_settle_unit'])

    def settle(self):
        now = datetime.datetime.now()
        delta_seconds = (now - self.last_reporting_time).seconds
        self.used_seconds += delta_seconds
        self.last_reporting_time = now
        units = self.used_seconds / app_config['cv_settle_unit_seconds']
        if units > 0:
            self.used_seconds -= units * 3600
            dv = units * app_config['cv_per_settle_unit']
            self.cost_contribution_value(dv)


class UserSiteManager(object):
    """
    管理用户正在使用的网站账号
    """

    user_sites = None

    def __init__(self):
        self.user_sites = {}

    def set_account(self, user_id, site_id, account):
        if user_id in self.user_sites \
                and site_id in self.user_sites[user_id]:
            user_site = self.user_sites[user_id][site_id]
            user_site.account_id = account.account_id

        user_site = UserSite(user_id, site_id, account)
        if user_id not in self.user_sites:
            self.user_sites[user_id] = {}
        self.user_sites[user_id][site_id] = user_site

    def get_account(self, user_id, site_id):
        if user_id not in self.user_accounts \
                or site_id not in self.user_accounts[user_id]:
            return None
        else:
            return self.user_accounts[user_id][site_id].account

    def remove_account(self, user_id, site_id):
        if user_id not in self.user_sites \
                or site_id not in self.user_sites[user_id]:
            return None
        else:
            del self.user_sites[user_id][site_id]

    def settle(self, user_id, site_id):
        if user_id in self.user_sites \
                and site_id in self.user_sites:
            self.user_sites[user_id][site_id].settle()

# TODO
# 后期加锁
class Manager(object):
    """
    维护网站/账号/用户之间关系
    """

    account_manager = None
    """
    账号管理器
    type: AccountManager
    """

    site_account_manager = None
    """
    网站账号管理器
    type: SiteAccountManager
    """

    user_site_manager = None
    """
    用户当前使用的网站
    type: UserSiteManager
    """

    validating_account_manager = None
    """
    正在添加/修改,处于验证过程的账号管理器
    type: AccountManager
    """

    running = True

    def __init__(self):
        self.account_manager = AccountManager()
        self.site_account_manager = SiteAccountManager()
        self.user_site_manager = UserSiteManager()
        self.validating_account_manager = AccountManager()
        self.load_accounts()

    def load_accounts(self):
        conn = db.connection()
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
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
            print account
            new_account = Account(
                site_id=account['site_id'],
                account_id=account['account_id'],
                owner_user_id=account['user_id'],
                username=account['username'],
                password=account['password'],
                max_concurrency_user=account['max_concurrency_user'])
            self.account_manager.add_account(new_account)
            self.site_account_manager.add_account(new_account)
            new_account.login(run_async=True)
        cur.close()
        conn.close()

    def is_user_using_site(self, user_id, site_id):
        """
        用户是否正在使用网站的账号
        :rtype: bool
        """
        return self.user_site_manager.get_account(user_id, site_id) is not None

    def pick_one_site_account(self, user_id, site_id):
        """
        随机从当前网站可能可以用的账号随机选择一个
        这个账号可能直接可以用，也有可能需要输入验证码
        :rtype: Account
        """
        original_account = self.user_account_manager.get(user_id, site_id)
        avaliable_accounts = list()
        for account in self.site_account_manager.get_accounts(site_id):
            if original_account and original_account.account_id == account.account_id:
                continue
            if account.site.status in [
                    site.STATUS_NEED_VERIFICATION,
                    site.STATUS_VALID_ACCOUNT]:
                avaliable_accounts.append(account)
        if len(avaliable_accounts) == 0:
            return None
        else:
            return random.choice(avaliable_accounts)

    def start_renting_account(self, user_id, account):
        """
        开始使用/切换账号
        """
        self.stop_renting_account(self, user_id, account.site_id)
        self.user_site_manager.add_site(user_id, account.site_id, account)
        account.users.append(user_id)

    def stop_renting_account(self, user_id, site_id):
        """
        停止使用账号
        """
        renting_account = self.user_site_manager.get(user_id, site_id)
        if renting_account:
            self.user_site_manager.settle(user_id, site_id)
            renting_account.users.remove(user_id)
            self.user_site_manager.remove_account(user_id, site_id)

    def user_report(self, user_id, site_id, in_user):
        if in_user:
            self.user_site_manager.settle(user_id, site_id)
        else:
            account = self.user_site_manager.get_account(user_id, site_id)
            account.remove_user(user_id)
            self.user_site_manager.remove_account(user_id, site_id)

    def _settle(self):
        """
        结算逻辑
        """
        while(self.running):
            time.sleep(datetime.timedelta(minutes=15).seconds)
            now = datetime.datetime.now()
            # 清理过久未上报状态的用户账号的状态
            for user_id, user_site in self.user_site_manager.user_sites.iteritems():
                delta_seconds = now - user_site.last_eporting_time
                if delta_seconds > 1000:
                    self.user_site_manager.remove_site(
                        user_id, user_site.site_id)
                    self.account_manager.get_account(
                        user_site.account_id).remove_user(user_id)

            # 结算账号拥有者
            for account in self.account_manager.get_accounts():
                account.settle()

    def start_periodly_settle(self):
        t = threading.Thread(target=self._settle, args=())
        t.daemon = False
        t.start()

    def stop_periodly_settle(self):
        self.running = False

manager = Manager()
