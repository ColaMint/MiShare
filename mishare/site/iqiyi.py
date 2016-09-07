#!/usr/bin/python
# -*- coding:utf-8 -*-

from site_base import SiteBase
import time

class Iqiyi(SiteBase):

    def _login(self):
        self.driver.get('http://www.iqiyi.com/')

        loggin_btn = self.driver.find_element_by_css_selector('div.usrTx-login > a')
        loggin_btn.click();

        input_username = self.driver.find_element_by_css_selector('.acountBorder[data-loginbox-elem=emailWrap] > input')
        input_username.send_keys(self.username)

        outside = self.driver.find_element_by_css_selector('#qipaLoginIfr > div:nth-child(1) > div > div.userLogin-title > h2')
        outside.click()

        input_password = self.driver.find_element_by_css_selector('.acountBorder[data-loginbox-elem=passwdWrap] > input')
        input_password.send_keys(self.password)

        # 不要记住账号密码
        #remember_me

        loggin_btn = self.driver.find_element_by_css_selector('a[data-loginbox-elem=loginBtn]')
        loggin_btn.click();

        # 通过异常捕获检查是否有验证码相关节点
        try:
            verification_code = self.driver.find_element_by_css_selector('span.yzimg[data-loginbox-elem=piccode] > img')
            self._save_verification_code()
        except Exception:
            pass

    def _save_verification_code(self):
        # 等待验证码图片加载完成
        time.sleep(5)
        verification_code = self.driver.find_element_by_css_selector('span.yzimg[data-loginbox-elem=piccode] > img')
        self.verification_code_png_base64 = self._element_screenshot_png_base64(verification_code)

    def refresh_cerification_code(self):
        refresh_btn = self.driver.find_element_by_css_selector('i.refreshIcon[data-loginbox-elem=refreshPiccode]')
        refresh_btn.click()
        self._save_verification_code()

    def _input_verification_code(self, verification_code):
        verification_code_input = self.driver.find_element_by_css_selector('input[data-loginbox-elem=piccodeInput]')
        verification_code_input.send_keys(verification_code)
        loggin_btn = self.driver.find_element_by_css_selector('a[data-loginbox-elem=loginBtn]')
        loggin_btn.click();

    def _save_vip_expire_timestamp(self):
        # TODO
        return 1480953735

    def _validate_cookies(self):
        """
        验证cookies是否有效
        :rtype: boolean
        """
        for cookie in self.cookies:
            if cookie['name'] == 'P000email' \
                and cookie['value'] == self.username:
                return True
        return False
