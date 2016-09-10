#!/usr/bin/python
# -*- coding:utf-8 -*-


from mishare.site import site
from mishare.site.iqiyi import Iqiyi
from mishare.site.youku import Youku
from mishare.lib.database import db
from mishare.etc.config import app as app_config
import datetime
import MySQLdb
import threading
import random
import time

class Engine(object):


