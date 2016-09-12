#!/usr/bin/python
# -*- coding:utf-8 -*-
from selenium import webdriver
from PIL import Image
import abc
import base64
import StringIO
import time
import threading
import Queue

STATUS_NO_LOGIN                     = 1
STATUS_NEED_VERIFICATION            = 2
STATUS_USERNAME_OR_PASSWORD_ERROR   = 3
STATUS_VERIFICATION_ERROR           = 4
STATUS_VALID_ACCOUNT                = 5
STATUS_INVALID_ACCOUNT              = 6

SITE_ID_IQIYI   = 1
SITE_ID_YOUKU   = 2
SITE_ID_TENCENT = 3

class Operation(object):

    op = None

    data = None

    def __init__(self, op, data=None):
        self.op = op
        self.data = data


class Site(object):
    """
    获取网站登录后cookie的抽象基本类
    """

    status = None
    """
    状态
    type: int
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

    vip_expire_timestamp = None
    """
    会员截止时间戳
    type: float
    """

    verification_code_queue = None

    def __init__(self, username, password):
        """
        :type username: string 用户名
        :type password: string 密码
        :rtype: None
        """
        self.status = STATUS_NO_LOGIN
        self.username = username
        self.password = password
        self.verification_code_queue= Queue.Queue()

        t = threading.Thread(target=self.driver_thread, args=())
        t.daemon = False
        t.start()

    def driver_thread(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1024, 800)
        self.login()
        while(True):
            verification_code = self.verification_code_queue.get()
            self.input_verification_code_help(verification_code=verification_code)

    def login(self):
        """
        执行登录操作
        检查账号密码是否错误
        检查是否需要验证码
        若登陆成功，检查账号是否有效
        :rtype: None
        """
        self._login()
        if self._is_username_or_password_error():
            self.status = STATUS_USERNAME_OR_PASSWORD_ERROR
        elif self._need_verification_code():
            self._save_verification_code()
            self.status = STATUS_NEED_VERIFICATION
        else:
            self._validate()

    abc.abstractmethod
    def _login(self):
        """
        执行登录操作
        :rtype: None
        """
        pass

    abc.abstractmethod
    def _is_username_or_password_error(self):
        """
        用户名或密码错误
        :rtype: bool
        """
        pass

    abc.abstractmethod
    def _need_verification_code(self):
        """
        是否需要验证码
        :rtype: bool
        """
        pass

    abc.abstractmethod
    def _is_verification_code_error(self):
        """
        验证码是否错误
        :rtype: bool
        """
        pass

    abc.abstractmethod
    def _save_verification_code(self):
        """
        获取验证码图片, 保存在self.verification_code_png_base64
        :rtype: None
        """
        pass

    def input_verification_code(self, verification_code, wait=5):
        """
        输入验证码，点击登录，验证账号有效性
        :type verification_code: string 验证码
        :rtype: None
        """
        self.verification_code_queue.put(verification_code)
        time.sleep(wait)

    def input_verification_code_help(self, verification_code):
        """
        输入验证码，点击登录，验证账号有效性
        :type verification_code: string 验证码
        :rtype: None
        """
        self._input_verification_code(verification_code)
        if self._is_username_or_password_error():
            self.status = STATUS_USERNAME_OR_PASSWORD_ERROR
        if self._is_verification_code_error():
            self._save_verification_code()
            self.status = STATUS_VERIFICATION_ERROR
        else:
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

    def _save_cookies(self, delay_seconds=5):
        """
        延迟获取cookie, 保存在self.cookies
        :rtype: None
        """
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        self.cookies = self.driver.get_cookies()

    abc.abstractmethod
    def _save_vip_expire_timestamp(self):
        pass

    def _validate(self):
        """
        验证cookie与vip的有效性, 将结果保存在seld.valid
        :rtype: None
        """
        self._save_cookies(3)
        if not self._validate_cookies():
            self.status = STATUS_INVALID_ACCOUNT
            return

        self._save_vip_expire_timestamp()
        if self.vip_expire_timestamp <= time.time():
            self.status = STATUS_INVALID_ACCOUNT
            return

        self.status = STATUS_VALID_ACCOUNT

    def _element_screenshot_png_base64(self, element):
        """
        获取节点的图片的base64编码字符串
        :type element: selenium.webdriver.remote.webelement.WebElement
        :rtype: string
        """
        location = element.location
        size = element.size
        left = int(location['x'])
        top = int(location['y'])
        right = int(left + size['width'])
        bottom = int(top + size['height'])
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
