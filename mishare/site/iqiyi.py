#!/usr/bin/python
# -*- coding:utf-8 -*-

from site_base import SiteBase
import time

class Iqiyi(SiteBase):

    def login(self, username, password):
        self.driver.get('http://www.iqiyi.com/')

        loggin_btn = self.driver.find_element_by_css_selector('div.usrTx-login > a')
        loggin_btn.click();

        input_username = self.driver.find_element_by_css_selector('.acountBorder[data-loginbox-elem=emailWrap] > input')
        input_username.send_keys(username)

        outside = self.driver.find_element_by_css_selector('#qipaLoginIfr > div:nth-child(1) > div > div.userLogin-title > h2')
        outside.click()

        input_password = self.driver.find_element_by_css_selector('.acountBorder[data-loginbox-elem=passwdWrap] > input')
        input_password.send_keys(password)

        loggin_btn = self.driver.find_element_by_css_selector('a[data-loginbox-elem=loginBtn]')
        loggin_btn.click();

        # 等待生成完整cookie
        time.sleep(3)

        self.cookies = self.driver.get_cookies()
        self.driver.quit()
