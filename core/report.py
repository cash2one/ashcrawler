# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

# libraries
import socket
import smtplib
from pymongo import MongoClient
from core.settings import EMAIL_PASSWORD
from log import *


def brief_report(settings):
    pis = settings['pis']
    project = settings['project']
    address = settings['address']
    port = settings['port']

    sender = 'snsgis@gmail.com'
    username = 'snsgis@gmail.com'
    t = datetime.datetime.now().strftime('%Y-%m-%d')

    pi_str = ''
    for pi in pis:
        pi_str += (pi + ';')

    now = datetime.datetime.now()
    utc_now_1 = now - datetime.timedelta(days=1)
    utc_now_2 = now - datetime.timedelta(days=2)
    utc_now_5 = now - datetime.timedelta(days=7)

    # For page information
    client = MongoClient(address, port)
    db = client[project]

    total_posts = db.pages.find().count()

    count_1 = db.pages.find({"created_at": {"$gt": utc_now_1}}).count()
    count_2 = db.pages.find({"created_at": {"$gt": utc_now_2}}).count()
    count_7 = db.pages.find({"created_at": {"$gt": utc_now_5}}).count()
    count_baidu_1  = db.pages.find({"$and": [{"type": "baidu"}, {"created_at": {"$gt": utc_now_2}}]}).count()
    count_google_1 = db.pages.find({"$and": [{"type": "google"}, {"created_at": {"$gt": utc_now_2}}]}).count()
    count_wechat_1 = db.pages.find({"$and": [{"type": "wechat"}, {"created_at": {"$gt": utc_now_2}}]}).count()

    line_1 = "Total records: %d" % total_posts
    line_2 = "In the last 24 hours: %d (baidu: %d, google: %d, wechat: %d) were collected ." % (count_1, count_baidu_1, count_google_1, count_wechat_1)
    line_3 = "In the last 2 days: %d were collected." % count_2
    line_4 = "In the last week: %d were collected." % count_7

    msg = '''From: Ash Crawling Server <snsgis@gmail.com>
To: ''' + pi_str[:-1] + '''
Subject: [''' + t + '''] Daily Briefing for the ''' + project.capitalize() + ''' Project
MIME-Version: 1.0

Dear project members,

Here is a briefing about the crawling progress:

     ''' + line_1 + '''
     ''' + line_2 + '''
     ''' + line_3 + '''
     ''' + line_4 + '''
--
Sent from the Ash Crawling Server.'''
    # The actual mail send
    try:
        server = smtplib.SMTP()
        server.connect('smtp.gmail.com', '587')
        server.ehlo()
        server.starttls()
        server.login(username, EMAIL_PASSWORD)
        server.sendmail(sender, pis, msg)
        server.quit()
    except socket.gaierror, e:
        print str(e) + "/n error raises when sending E-mails."
