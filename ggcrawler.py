# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Apr 2, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import os
import sys
from core.google import ggcrawler
from core.log import *
from settings import SETTINGS

current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)


keywords = [
    '捐赠 元',
    '捐赠 万元 OR 亿元',
    '捐赠 元 小学 OR 中学 OR 大学 OR 学校 OR 学院 OR 班',
    '捐赠 元 集团 OR 有限公司 OR 有限责任公司 OR 基金会 -学校 -学院 -小学 -中学 -大学 -班'
]

start = datetime.datetime.now()
log(NOTICE, 'Google Crawler Initializing...')
for keyword in keywords:
    ggcrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'], SETTINGS['username'], SETTINGS['password'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
