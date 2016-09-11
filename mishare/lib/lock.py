#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading

class Lock(object):

    lock = None
    """
    :type: threading.Lock
    """

    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
        if exc_value is not None:
            raise exc_value
