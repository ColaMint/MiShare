#!/usr/bin/python
# -*- coding:utf-8 -*-

from site import Site
import time

class Iqiyi(Site):

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

    def _is_username_or_password_error(self):
        try:
            time.sleep(1)
            error_area = self.driver.find_element_by_css_selector('#qipaLoginIfr > div:nth-child(1) > div > div.usrTxGeneral-box_v3.box_v3AddCode > div.logReg-form > div')
            return u'密码' in error_area.text
        except Exception:
            return False

    def _need_verificaton_code(self):
        try:
            verification_code = self.driver.find_element_by_css_selector('span.yzimg[data-loginbox-elem=piccode] > img')
            self._save_verification_code()
            return True
        except Exception:
            return False

    def _is_verification_code_error(self):
        try:
            time.sleep(1)
            error_area = self.driver.find_element_by_css_selector('#qipaLoginIfr > div:nth-child(1) > div > div.usrTxGeneral-box_v3.box_v3AddCode > div.logReg-form > div')
            return u'验证码' in error_area.text
        except Exception:
            return False

    def _save_verification_code(self):
        # 等待验证码图片加载完成
        time.sleep(3)
        verification_code = self.driver.find_element_by_css_selector('span.yzimg[data-loginbox-elem=piccode] > img')
        self.verification_code_png_base64 = self._element_screenshot_png_base64(verification_code)

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
