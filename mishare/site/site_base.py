#!/usr/bin/python
# -*- coding:utf-8 -*-
from selenium import webdriver
import abc

class SiteBase(object):

    driver = None
    """
    浏览器引擎
    """

    cookies = None
    """
    登陆成功后的cookie
    """

    valid = None
    """
    用户是否有效(密码正确+拥有会员)
    """

    vip_end_time = None
    """
    会员截止时间
    """

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    abc.abstractmethod
    def login(self, username, password):
        pass
