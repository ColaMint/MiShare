#!/usr/bin/python
# -*- coding:utf-8 -*-

from site import Site
import time

class Youku(Site):

    def _login(self):
        self.driver.get('http://www.youku.com/')

        loggin_btn = self.driver.find_element_by_css_selector('#qheader_login')
        loggin_btn.click();

        input_username = self.driver.find_element_by_css_selector('#YT-ytaccount')
        input_username.send_keys(self.username)

        input_password = self.driver.find_element_by_css_selector('#YT-ytpassword')
        input_password.send_keys(self.password)

        # 不要记住账号密码
        remember_me = self.driver.find_element_by_css_selector('#YT-ytremember')
        if remember_me.get_attribute('checked') == 'checked':
            remember_me.click()

        loggin_btn = self.driver.find_element_by_css_selector('#YT-nloginSubmit')
        loggin_btn.click();

        # 通过异常捕获检查是否有验证码相关节点
        try:
            verification_code = self.driver.find_element_by_css_selector('#YT-captchaImg')
            self._save_verification_code()
        except Exception:
            pass

    def _is_username_or_password_error(self):
        try:
            time.sleep(1)
            error_area = self.driver.find_element_by_css_selector('#YT-errorTips')
            return u'密码' in error_area.text
        except Exception:
            return False

    def _need_verificaton_code(self):
        try:
            verification_code = self.driver.find_element_by_css_selector('#YT-captchaImg')
            return True
        except Exception:
            return False

    def _is_verification_code_error(self):
        try:
            time.sleep(1)
            error_area = self.driver.find_element_by_css_selector('#YT-errorTips')
            return u'验证码' in error_area.text
        except Exception:
            return False

    def _save_verification_code(self):
        # 等待验证码图片加载完成
        time.sleep(3)
        verification_code = self.driver.find_element_by_css_selector('#YT-captchaImg')
        self.verification_code_png_base64 = self._element_screenshot_png_base64(verification_code)

    def _input_verification_code(self, verification_code):
        verification_code_input = self.driver.find_element_by_css_selector('#YT-captcha')
        verification_code_input.send_keys(verification_code)
        loggin_btn = self.driver.find_element_by_css_selector('#YT-nloginSubmit')
        loggin_btn.click();

    def _save_vip_expire_timestamp(self):
        # TODO
        self.vip_expire_timestamp = 1480953735

    def _validate_cookies(self):
        """
        验证cookies是否有效
        :rtype: boolean
        """
        for cookie in self.cookies:
            if cookie['name'] == 'P_sck' \
                and len(cookie['value']) > 0:
                return True
        return False
