# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Apr 2, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import sys
import os
from core.wechat import wccrawler
from core.log import *
from settings import SETTINGS

current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)

keywords = ['捐赠 元', '慈善']

start = datetime.datetime.now()
log(NOTICE, 'Wechat Crawler Initializing...')
for keyword in keywords:
    wccrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'], SETTINGS['username'], SETTINGS['password'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
