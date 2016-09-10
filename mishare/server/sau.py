#!/usr/bin/python
# -*- coding:utf-8 -*-

class SAU(object):

    def __init__(self, site_id, account_id, user_id):
        self.site_id    = site_id
        self.account_id = account_id
        self.user_id = site_id

class SAUManager(object):
    """
    维护 site_id, account_id, user_id 三元组
    """

    sau = None
    """
    :type: set
    """

    def __init__(self):
        self.sau = set()

    def add(self, site_id , account_id, user_id):
        self.sau.add((site_id, account_id, user_id))

    def search(self, site_id=None, account_id=None, user_id=None):
        results = []
        for s, a, u in self.sau.iteritems():
            if site_id is not None and s != site_id:
                continue
            if account_id is not None and a != account_id:
                continue
            if user_id is not None and u != user_id:
                continue
            results.append(SAU(s, a, u))
        return results

    def remove(self, site_id=None, account_id=None, user_id=None):
        for r in self.search(site_id, account_id, user_id):
            self.sau.discard(r)

    def clear(self):
        self.sau.clear()
