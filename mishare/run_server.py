#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../../')))
from mishare.server.app import app
from mishare.server.router import account, site, user
from mishare.etc.config import server

app.run(
    host=server['host'],
    port=server['port'],
    debug=server['debug'])
