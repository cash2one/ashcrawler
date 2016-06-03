# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 25, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import sys
import os
from core.baidu import bdcrawler
from core.log import *
from settings import SETTINGS

current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)

keywords = [
    '"捐赠 元"',
    '"捐赠 万元" | "捐赠 亿元"',
    '"捐赠 元 小学" | "捐赠 元 中学" | "捐赠 元 大学"',
    '"捐赠 元 学校" | "捐赠 元 学院" | "捐赠 元 班"',
    '"捐赠 元 集团" | "捐赠 元 有限公司" | "捐赠 元 基金会"',
    '"捐赠 元 总经理" | "捐赠 元 董事长"'
    ]

start = datetime.datetime.now()
log(NOTICE, 'Baidu Crawler Initializing...')
for keyword in keywords:
    bdcrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'], SETTINGS['username'], SETTINGS['password'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
