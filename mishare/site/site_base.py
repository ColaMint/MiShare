#!/usr/bin/python
# -*- coding:utf-8 -*-
from selenium import webdriver
import abc
from PIL import Image
import base64
import StringIO
import time

class SiteBase(object):
    """
    获取网站登录后cookie的抽象基本类
    """

    username = None
    """
    用户名
    type: string
    """

    password = None
    """
    密码
    type: string
    """

    driver = None
    """
    浏览器引擎
    :type: selenium.webdriver.chrome.webdriver.WebDriver
    """

    verification_code_png_base64 = None
    """
    验证码图片base64编码字符串
    type: string
    """

    cookies = None
    """
    登陆后的cookie
    type: list
    """

    valid = None
    """
    用户是否有效(密码正确+拥有会员)
    type: bool
    """

    vip_expire_timestamp = None
    """
    会员截止时间戳
    type: float
    """

    def __init__(self, username, password):
        """
        :type username: string 用户名
        :type password: string 密码
        :rtype: None
        """
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1024, 800)

    def login(self):
        """
        执行登录操作
        若不需要验证码，校验账号的有效性
        否则，保存验证码图片，需要进一步输入验证码
        :rtype: None
        """
        self._login()
        if self.need_verification_code:
            return
        self._validate()

    abc.abstractmethod
    def _login(self):
        """
        执行登录操作
        若不需要验证码，直接返回
        否则，保存验证码图片
        :rtype: None
        """
        pass

    abc.abstractmethod
    def _save_verification_code(self):
        """
        获取验证码图片, 保存在self.verification_code_png_base64
        :rtype: None
        """
        pass

    abc.abstractmethod
    def refresh_cerification_code(self):
        """
        刷新验证码图片, 保存在self.verification_code_png_base64
        :rtype: None
        """
        pass

    def input_verification_code(self, verification_code):
        """
        输入验证码，点击登录，验证账号有效性
        :type verification_code: string 验证码
        :rtype: None
        """
        self._input_verification_code(verification_code)
        self._validate()

    abc.abstractmethod
    def _input_verification_code(self, verification_code):
        """
        输入验证码，点击登录
        :type verification_code: string 验证码
        :rtype: None
        """
        pass

    abc.abstractmethod
    def _get_vip_expire_timestamp(self):
        """
        获取会员到期时间戳, 保存在self.vip_expire_timestamp
        :rtype: None
        """
        pass

    abc.abstractmethod
    def _validate_cookies(self):
        """
        验证cookies是否有效
        :rtype: boolean
        """
        pass

    @property
    def need_verification_code(self):
        """
        是否需要验证码
        :rtype: boolean
        """
        return self.verification_code_png_base64 is not None

    def _save_cookies(self, delay_seconds=5):
        """
        延迟获取cookie, 保存在self.cookies
        :rtype: None
        """
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        self.cookies = self.driver.get_cookies()

    def _validate(self):
        """
        验证cookie与vip的有效性, 将结果保存在seld.valid
        :rtype: None
        """
        self._save_cookies()
        if not self._validate_cookies():
            self.valid = False
            return

        self._save_vip_expire_timestamp()
        if self.vip_expire_timestamp <= time.time():
            self.valid = False
            return

        self.valid = True

    def _element_screenshot_png_base64(self, element):
        """
        获取节点的图片的base64编码字符串
        :type element: selenium.webdriver.remote.webelement.WebElement
        :rtype: string
        """
        location = element.location
        size     = element.size
        left     = int(location['x'])
        top      = int(location['y'])
        right    = int(left + size['width'])
        bottom   = int(top + size['height'])
        buff = StringIO.StringIO()
        img = Image.open(
            StringIO.StringIO(
                base64.b64decode(
                    self.driver.get_screenshot_as_base64()
                )
            )
        )
        img = img.crop((left, top, right, bottom))
        img.save(buff, format='PNG')
        base64_string = base64.b64encode(buff.getvalue())
        buff.close()
        return base64_string

    def close(self):
        """
        关闭浏览器引擎
        """
        self.driver.close()
