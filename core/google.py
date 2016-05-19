# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Apr 2, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import urllib
import platform
from pymongo import MongoClient, errors
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from log import *
from settings import TIMEOUT, TZCHINA
import datetime
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


# Crawling pages from Google.com
def ggcrawler(keyword, project, address, port, username, password):
    start = datetime.datetime.now()
    log(NOTICE, 'Crawling Google with keyword %s....' % keyword)
    if "Linux" in platform.platform():
        browser = webdriver.PhantomJS(executable_path=r'/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    else:
        browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    # firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    #
    # browser = webdriver.Firefox(firefox_profile=firefox_profile)
    #
    # browser.set_window_size(960, 1050)
    # browser.set_window_position(0, 0)

    browser.set_page_load_timeout(TIMEOUT)

    client = MongoClient(address, port)
    db = client[project]
    db.authenticate(username, password)

    base_url = "https://www.google.com/?gws_rd=ssl#tbs=qdr:d&q="
    i = 0
    while i == 0 or len(soup.find_all('div', class_='g')) != 0:
        # print soup.find_all('a', class_='n')[-1].text
        if i >= 15:
            break
        url = base_url + urllib.quote(keyword) + '&start=' + str(i * 10)
        log(NOTICE, '===============Parsing Page %d===============' % (i + 1))

        try:
            browser.get(url)
            time.sleep(2)
        except TimeoutException:
            # print 'time out after %d seconds when loading page' % TIMEOUT
            browser.execute_script('window.stop()')

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('div', class_='g')
        # print url
        t_china = datetime.datetime.now(TZCHINA)
        for item in items:
            try:
                title = item.find('h3').text.encode('utf-8', 'ignore')
                url = str(item.find('h3').find('a').attrs['href'])[7:].split("&sa=")[0]
                orig_url = url
                # time_before = item.find('span', class_='f').text
                abstract = item.find('span', class_='st').text
                log(NOTICE, '%s from %s at %s' % (str(title), orig_url, str(t_china)))
            except AttributeError:
                log(WARNING, 'find an unusual page.')
                continue
            page_json = {
                "type": "google",
                "keyword": keyword,
                "title": title.strip(),
                "abstract": abstract.strip(),
                "orig_url": url,
                "url": url,
                "created_at": t_china
            }
            # "time_before": time_before
            try:
                db.pages.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')
        i += 1

    browser.close()
    log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - start).seconds)))
