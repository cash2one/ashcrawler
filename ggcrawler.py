# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Apr 2, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from ashcrawler.google import ggcrawler
from ashcrawler.log import *
from settings import SETTINGS
import datetime
import sys

#sys.path.append("/home/ubuntu/.local/lib/python2.7/site-packages")
sys.path.append("/home/ubuntu/ashcrawler")


keywords = ['捐赠 元', '慈善']

start = datetime.datetime.now()
log(NOTICE, 'Google Crawler Initializing...')
for keyword in keywords:
    ggcrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
