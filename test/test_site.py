#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../../')))
import unittest
from mishare.site.iqiyi import Iqiyi


class TestSite(unittest.TestCase):

    def test_iqiyi(self):
        iqiyi = Iqiyi()
        iqiyi.login('13710230105', '03545328')

if __name__ == '__main__':
    unittest.main()
