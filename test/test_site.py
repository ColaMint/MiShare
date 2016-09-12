#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../../')))
import unittest
from mishare.site import site
from mishare.site.iqiyi import Iqiyi
from mishare.site.youku import Youku
from mishare.site.manager import Manager
import time


class TestSite(unittest.TestCase):

    def test_all_sites(self):
        return
        sites = [
            (Iqiyi, '13710230105', '03545328'),
            (Youku, '13710230105', 'slmy03545328'),
            (Tencent, '754281128', 'CHIchi754281128'),
        ]
        for ss in sites:
            s = ss[0](ss[1], ss[2])
            self.assertEqual(site.STATUS_NO_LOGIN, s.status)
            s.login()
            self.assertIn(s.status,
                [   site.STATUS_NEED_VERIFICATION,
                    site.STATUS_VALID_ACCOUNT,
                    site.STATUS_INVALID_ACCOUNT])
            if s.status == site.STATUS_NEED_VERIFICATION:
                self.assertIsNone(s.cookies)
                self.assertIsNone(s.vip_expire_timestamp)

                c1 = s.verification_code_png_base64
                self.assertGreater(len(c1), 0)

                s.input_verification_code('test')
                self.assertEqual(site.STATUS_VERIFICATION_ERROR, s.status)

                c2 = s.verification_code_png_base64
                self.assertGreater(len(c2), 0)
            elif s.status == site.STATUS_VALID_ACCOUNT:
                self.assertGreater(s.vip_expire_timestamp, 0)
                self.assertGreater(len(s.cookies), 0)
            s.close()

            s = ss[0](ss[1], 'test')
            self.assertEqual(site.STATUS_NO_LOGIN, s.status)
            s.login()
            self.assertIn(s.status,
                [   site.STATUS_USERNAME_OR_PASSWORD_ERROR,
                    site.STATUS_NEED_VERIFICATION])
            s.close()

    def test_manager(self):
        manager = Manager()
        manager.start_periodly_settle(run_async=True)

        user_id = 5
        site_id = 1
        self.assertFalse(manager.is_user_using_site(user_id, site_id))


if __name__ == '__main__':
    unittest.main()
