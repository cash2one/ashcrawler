# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from random import randint
import time
from selenium.common.exceptions import TimeoutException
from log import *
from pymongo import MongoClient


def get_interval_as_human(low=1, high=3):
    return randint(low, high)


def get_response_as_human(browser, url, page_reload=True, waiting=-1):
    url_raw = url
    response_data = ''
    if waiting == -1:
        waiting = get_interval_as_human()
    if page_reload:
        while True:
            try:
                time.sleep(waiting)
                browser.get(url_raw)
                response_data = browser.page_source
                if response_data != {}:
                    break
            except TimeoutException:
                url_raw = browser.current_url
                log(NOTICE, 'Web page refreshing')
    else:
        try:
            time.sleep(waiting)
            browser.get(url_raw)
            response_data = browser.page_source
        except TimeoutException:
            log(WARNING, 'timeout', 'get_response_as_human')
    return response_data


def get_as_human(browser, url, page_reload=True, waiting=-1):
    url_raw = url
    if waiting == -1:
        waiting = get_interval_as_human()
    if page_reload:
        while True:
            try:
                time.sleep(waiting)
                browser.get(url_raw)
                response_data = browser.page_source
                if response_data != {}:
                    break
            except TimeoutException:
                url_raw = browser.current_url
                log(NOTICE, 'Web page refreshing')
    else:
        try:
            time.sleep(waiting)
            browser.get(url_raw)
        except TimeoutException:
            log(WARNING, 'timeout', 'get_as_human')
    return browser


def del_duplicates(settings):

    project = settings['project']
    address = settings['address']
    port = settings['port']
    username = settings['username']
    password = settings['password']

    # Within the last 24 hours
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=1000)

    # For page information
    client = MongoClient(address, port)
    db = client[project]
    # db.authenticate(username, password)

    pages = db.pages.find({"created_at": {"$gt": start}})

    titles = []
    for page in pages:
        temp = page['title']
        if len(temp) >= 8:
            title = page['title'].replace(" ", "").strip()[:8]
            print title
            titles.append(title)
    titles = sorted(titles)
    uniques = set(titles)
    log(NOTICE, "data list created")

    for unique in uniques:
        titles.remove(unique)
    log(NOTICE, "remove the uniques")

    for title in titles:
        db.pages.delete_one({'title': {'$regex': title}})
    log(NOTICE, "completed")


# tag 1：亿、千万、百万、十万
# tag 2：募捐、扶贫济困日、慈善日
# tag 3: name list in the this email
def add_tags(settings):

    project = settings['project']
    address = settings['address']
    port = settings['port']
    username = settings['username']
    password = settings['password']

    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=1000)

    # For page information
    client = MongoClient(address, port)
    db = client[project]
    db.authenticate(username, password)

    for tag in [u"亿", u"千万", u"百万", u"十万"]:
        log(NOTICE, "processing tag %s" % tag)
        pages = db.pages.find({"$and": [{"created_at": {"$gt": start}}, {'abstract': {'$regex': tag}}]})
        # i = 0
        for page in pages:
            db.pages.update({'_id': page['_id']}, {'$set': {'unit': tag}})
            # i += 1
            # print i
        log(NOTICE, "tagging unit completed.")

    for tag in [u"募捐", u"扶贫济困日", u"慈善日"]:
        log(NOTICE, "processing tag %s" % tag)
        pages = db.pages.find({"$and": [{"created_at": {"$gt": start}}, {'abstract': {'$regex': tag}}]})
        # i = 0
        for page in pages:
            db.pages.update({'_id': page['_id']}, {'$set': {'event': tag}})
            # i += 1
            # print i
        log(NOTICE, "tagging unit completed.")

    log(NOTICE, "completed")
