#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../../')))
import unittest
from mishare.site.iqiyi import Iqiyi
from mishare.site.youku import Youku


class TestSite(unittest.TestCase):

    def test_iqiyi(self):
        iqiyi = Iqiyi('13710230105', '03545328')
        iqiyi.login()
        if iqiyi.need_verification_code:
            self.assertIsNone(iqiyi.valid)
            self.assertIsNone(iqiyi.cookies)
            self.assertIsNone(iqiyi.vip_expire_timestamp)

            c1 = iqiyi.verification_code_png_base64
            self.assertGreater(len(c1), 0)

            iqiyi.refresh_cerification_code()
            c2 = iqiyi.verification_code_png_base64
            self.assertGreater(len(c2), 0)
            self.assertNotEqual(c1, c2)

            iqiyi.input_verification_code('test')
            self.assertGreater(len(iqiyi.cookies), 0)
            self.assertIsNone(iqiyi.vip_expire_timestamp)
            self.assertFalse(iqiyi.valid)

        else:
            self.assertIsNotNone(iqiyi.valid)
            if iqiyi.valid:
                self.assertGreater(iqiyi.vip_expire_timestamp, 0)
                self.assertGreater(len(iqiyi.cookies), 0)

        iqiyi.close()

    def test_youku(self):
        youku = Youku('13710230105', 'slmy03545328')
        youku.login()
        if youku.need_verification_code:
            self.assertIsNone(youku.valid)
            self.assertIsNone(youku.cookies)
            self.assertIsNone(youku.vip_expire_timestamp)

            c1 = youku.verification_code_png_base64
            self.assertGreater(len(c1), 0)

            youku.refresh_cerification_code()
            c2 = youku.verification_code_png_base64
            self.assertGreater(len(c2), 0)
            self.assertNotEqual(c1, c2)

            youku.input_verification_code('test')
            self.assertGreater(len(youku.cookies), 0)
            self.assertIsNone(youku.vip_expire_timestamp)
            self.assertFalse(youku.valid)

        else:
            self.assertIsNotNone(youku.valid)
            if youku.valid:
                self.assertGreater(youku.vip_expire_timestamp, 0)
                self.assertGreater(len(youku.cookies), 0)

        youku.close()

if __name__ == '__main__':
    unittest.main()
