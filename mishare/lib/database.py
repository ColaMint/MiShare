#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb

class Database(object):

    def __init__(self, host='localhost', user='root', port=3306, passwd='root', db='db'):
        self.host   = host
        self.port   = port
        self.user   = user
        self.passwd = passwd
        self.db     = db

    def connection(self):
        return MySQLdb.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db)
