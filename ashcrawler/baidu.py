# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 25, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import time
import urllib
import platform
from pymongo import MongoClient, errors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from log import *

from settings import TIMEOUT, TZCHINA
import datetime


# Crawling pages from Baidu.com
def bdcrawler(keyword, project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, 'Crawling Baidu with keyword %s....' % keyword)
    if "Linux" in platform.platform():
         browser = webdriver.PhantomJS(executable_path=r'/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    else:
        # browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')
        pass

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
    base_url = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd="
    # base_url = "http://www.baidu.com/s?wd="
    # log(NOTICE, "Total #: %d" % count)

    try:
        browser.get(base_url + urllib.quote(keyword))
    except TimeoutException:
        # print 'time out after %d seconds when loading page' % TIMEOUT
        browser.execute_script('window.stop()')

    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_tool')))
    browser.find_element_by_class_name('search_tool').click()
    time.sleep(2)
    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_tool_tf')))
    browser.find_element_by_class_name('search_tool_tf').click()
    log(NOTICE, 'Harvesting the new pages generated within the past 24 hours.')
    # time.sleep(2)
    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.LINK_TEXT, u'一天内')))
    browser.find_element_by_link_text(u'一天内').click()

    soup = BeautifulSoup(browser.page_source, 'html5lib')
    path_url = browser.current_url
    i = 0

    while i == 0 or soup.find_all('a', class_='n')[-1].text == u'下一页>':
        # print soup.find_all('a', class_='n')[-1].text
        url = path_url + '&pn=' + str(i * 10)
        log(NOTICE, '===============Parsing Page %d===============' % (i + 1))

        try:
            browser.get(url)
        except TimeoutException:
            # print 'time out after %d seconds when loading page' % TIMEOUT
            browser.execute_script('window.stop()')

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('div', class_='result c-container ')
        # print url
        t_china = datetime.datetime.now(TZCHINA)
        for item in items:
            try:
                title = item.find('h3').text
                time_before = item.find('span', class_=' newTimeFactor_before_abs m').text[:-3]
                abstract = item.find('div', class_='c-abstract').text[len(time_before)+3:]
                url = item.find('a', class_='c-showurl').attrs['href']
                orig_url = item.find('a', class_='c-showurl').text
                log(NOTICE, '%s from %s at %s' % (title, orig_url, str(t_china)))
            except AttributeError:
                log(WARNING, 'find an unusual page.')
                continue
            page_json = {
                "type": "baidu",
                "keyword": keyword,
                "title": title,
                "abstract": abstract,
                "orig_url": orig_url,
                "url": url,
                "created_at": t_china,
                "time_before": time_before
            }
            try:
                db.pages.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')
        i += 1

    browser.close()
    log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - start).seconds)))
