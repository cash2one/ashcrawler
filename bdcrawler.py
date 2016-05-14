# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 25, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from ashcrawler.baidu import bdcrawler
from ashcrawler.log import *
from settings import SETTINGS
import datetime
import sys

# sys.path.append("/home/ubuntu/.local/lib/python2.7/site-packages")
sys.path.append("/home/ubuntu/ashcrawler")

port = 27017
address = 'localhost'
project = 'philanthropy'

keywords = ['捐赠 元', '慈善']

start = datetime.datetime.now()
log(NOTICE, 'Baidu Crawler Initializing...')
for keyword in keywords:
    bdcrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
