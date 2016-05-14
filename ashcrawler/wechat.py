# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on April 12, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import time
import platform
from pymongo import MongoClient, errors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from log import *
from settings import TIMEOUT, TZCHINA
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

username = 'AshCenter'
password = 'ashcenter2016'


# Crawling pages from weixin.sogou.com
def wccrawler(keyword, project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, 'Crawling WeChat with keyword %s....' % keyword)

    if "Linux" in platform.platform():
        browser = webdriver.PhantomJS(executable_path=r'/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    else:
        browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    browser.set_page_load_timeout(TIMEOUT)

    client = MongoClient(address, port)
    db = client[project]
    base_url = "http://weixin.sogou.com/"

    while True:
        try:
            browser.get(base_url)
            break
        except TimeoutException:
            # print 'time out after %d seconds when loading page' % TIMEOUT
            # browser.execute_script('window.stop()')
            log(NOTICE, "refreshing...")

    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, 'loginBtn')))
    browser.find_element_by_id('loginBtn').click()

    time.sleep(2)
    browser.switch_to.frame(0)
    # browser.switch_to.frame(browser.find_element_by_id("ptlogin_iframe"))
    time.sleep(2)
    browser.switch_to.frame(0)
    time.sleep(2)
    browser.find_element_by_id('switcher_plogin').click()

    # input username
    user = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, 'u')))
    user.clear()
    user.send_keys(username, Keys.ARROW_DOWN)

    # input the passowrd
    passwd = browser.find_element_by_id('p')
    passwd.clear()
    passwd.send_keys(password, Keys.ARROW_DOWN)

    # press click and then the vcode appears.
    browser.find_element_by_class_name('login_button').click()

    try:
        time.sleep(3)
        browser.find_element_by_class_name('login_button').click()
    except:
        pass
    time.sleep(5)
    browser.switch_to.default_content()
    time.sleep(5)
    try:
        browser.find_element_by_id("indx-login")
    except:
        log(NOTICE, "unlogin")
    log(NOTICE, "login")

    # http://weixin.sogou.com/weixin?query=%E6%8D%90%E8%B5%A0+%E5%85%83&sourceid=inttime_day&type=2&page=3
    log(NOTICE, 'Harvesting the new pages generated within the past 24 hours.')
    while True:
        try:
            query = browser.find_element_by_id("upquery")
            query.clear()
            query.send_keys(keyword.decode('utf8'), Keys.ARROW_DOWN)
            browser.find_element_by_class_name('swz').click()
            time.sleep(5)
            break
        except TimeoutException:
            browser.refresh()
            log(NOTICE, 'refreshing')

    # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.LINK_TEXT, u'全部时间')))
    browser.find_element_by_link_text(u'全部时间').click()
    # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.LINK_TEXT, u'一天内')))
    time.sleep(2)
    browser.find_element_by_link_text(u'一天内').click()
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html5lib')
    i = 0
    while soup.find(id='sogou_next') is not None:
        soup = BeautifulSoup(browser.page_source, 'html5lib')
        t_china = datetime.datetime.now(TZCHINA)

        for item in soup.find_all("div", "txt-box"):
            try:
                title = item.find('h4').text
                url = u'http://weixin.sogou,com' + item.h4.a.attrs['href']
                abstract = item.p.text
                user_name = item.find("a", "wx-name").attrs['title']
                time_before = item.find("span", "time").text.split(")")[1]
            except AttributeError:
                log(WARNING, 'find an unusual page.')
                continue

            page_json = {
                "type": "wechat",
                "keyword": keyword,
                "title": title,
                "username": user_name,
                "abstract": abstract,
                "orig_url": url,
                "url": url,
                "created_at": t_china,
                "time_before": time_before
            }

            try:
                db.pages.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')
        i += 1
        print "page" + str(i) + " is processed: " + browser.current_url
        # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.LINK_TEXT, u'下一页')))
        try:
            browser.find_element_by_link_text(u'下一页').click()
            time.sleep(10)
        except NoSuchElementException:
            log(NOTICE, "Reaching the last page.")
            break
    browser.close()
    log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - start).seconds)))
