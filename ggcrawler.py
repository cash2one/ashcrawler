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
import datetime
import sys

sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/ashcrawler")

port = 27017
address = 'localhost'
project = 'cga'

keywords = ['捐赠 元', '慈善']

start = datetime.datetime.now()
log(NOTICE, 'Google Crawler Initializing...')
for keyword in keywords:
    ggcrawler(keyword, project, address, port)

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
