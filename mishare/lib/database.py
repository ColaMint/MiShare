#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import current_app
from mishare.etc.config import database
import MySQLdb


class Database(object):

    def __init__(
            self,
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            db='mishare'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def connection(self):
        return Connection(MySQLdb.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset='utf8'))

class Connection(object):

    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is None:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_value:
            raise exc_value


database = Database(
    host=database['host'],
    port=database['port'],
    user=database['user'],
    passwd=database['passwd'],
    db=database['db'])
