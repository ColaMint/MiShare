#!/usr/bin/python
# -*- coding:utf-8 -*-

from site import Site
import time
import traceback

class Tencent(Site):
    def _login(self):
        self.driver.get('http://v.qq.com/')

        # 弹出登陆窗
        login_btn = self.driver.find_element_by_css_selector('#mod_head_notice_trigger')
        login_btn.click()

        # 选择qq登陆
        qq_login_btn = self.driver.find_element_by_css_selector('div.login_btns > a.btn_qq')
        qq_login_btn.click()

        # 进入iframe
        self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#_login_frame_quick_'))

        # 不自动登陆
        auto_login_btn = self.driver.find_element_by_css_selector('#q_low_login_wording')
        auto_login_btn.click()

        # 切换账号登陆模式
        switch_mode_btn = self.driver.find_element_by_css_selector('#switcher_plogin')
        switch_mode_btn.click()

        input_username = self.driver.find_element_by_css_selector('#u')
        input_username.send_keys(self.username)

        input_password = self.driver.find_element_by_css_selector('#p')
        input_password.send_keys(self.password)

        login_btn = self.driver.find_element_by_css_selector('#login_button')
        login_btn.click()

    def _is_username_or_password_error(self):
        try:
            time.sleep(1)
            error_area = self.driver.find_element_by_css_selector('#err_m')
            return u'密码' in error_area.text
        except Exception:
            return False

    def _need_verification_code(self):
        try:
            self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#newVcodeIframe > iframe'))
            self.driver.find_element_by_css_selector('#capImg')
            return True
        except Exception as e:
            print e
            return False

    def _is_verification_code_error(self):
        try:
            self.driver.find_element_by_css_selector('#capImg')
            return True
        except Exception:
            return False

    def _save_verification_code(self):
        # 等待验证码图片加载完成
        time.sleep(3)
        verification_code = self.driver.find_element_by_css_selector('#capImg')
        self.verification_code_png_base64 = self._element_screenshot_png_base64(verification_code)

    def _input_verification_code(self, verification_code):
        verification_code_input = self.driver.find_element_by_css_selector('#capAns')
        verification_code_input.send_keys(verification_code)
        loggin_btn = self.driver.find_element_by_css_selector('#submit')
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
            print cookie
            if cookie['domain'] == '.qq.com' \
                and cookie['name'] == 'skey':
                return True
        return False
