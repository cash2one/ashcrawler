# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Apr 2, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import sys
import os
from core.wechat import wccrawler
from core.log import *
from settings import SETTINGS

current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)

keywords = [
    '捐赠 元 王|捐赠 元 李|捐赠 元 张|捐赠 元 刘|捐赠 元 陈|捐赠 元 杨|捐赠 元 黄',
    '捐赠 元 赵|捐赠 元 吴|捐赠 元 周|捐赠 元 徐|捐赠 元 孙|捐赠 元 马|捐赠 元 朱',
    '捐赠 元 胡|捐赠 元 郭|捐赠 元 何|捐赠 元 高|捐赠 元 林|捐赠 元 郑|捐赠 元 谢',
    '捐赠 元 罗|捐赠 元 梁|捐赠 元 宋|捐赠 元 唐|捐赠 元 许|捐赠 元 韩|捐赠 元 冯',
    '捐赠 元 邓|捐赠 元 曹|捐赠 元 彭|捐赠 元 曾|捐赠 元 萧|捐赠 元 田|捐赠 元 董',
    '捐赠 元 袁|捐赠 元 潘|捐赠 元 于|捐赠 元 蒋|捐赠 元 蔡|捐赠 元 余|捐赠 元 杜',
    '捐赠 元 叶|捐赠 元 程|捐赠 元 苏|捐赠 元 魏|捐赠 元 吕|捐赠 元 丁|捐赠 元 任',
    '捐赠 元 沈|捐赠 元 姚|捐赠 元 卢|捐赠 元 姜|捐赠 元 崔|捐赠 元 钟|捐赠 元 谭',
    '捐赠 元 陆|捐赠 元 汪|捐赠 元 范|捐赠 元 金|捐赠 元 石|捐赠 元 廖|捐赠 元 贾',
    '捐赠 元 夏|捐赠 元 韦|捐赠 元 付|捐赠 元 方|捐赠 元 白|捐赠 元 邹|捐赠 元 孟',
    '捐赠 元 熊|捐赠 元 秦|捐赠 元 邱|捐赠 元 江|捐赠 元 尹|捐赠 元 薛|捐赠 元 闫',
    '捐赠 元 段|捐赠 元 雷|捐赠 元 侯|捐赠 元 龙|捐赠 元 史|捐赠 元 陶|捐赠 元 黎',
    '捐赠 元 贺|捐赠 元 顾|捐赠 元 毛|捐赠 元 郝|捐赠 元 龚|捐赠 元 邵|捐赠 元 万',
    '捐赠 元 钱|捐赠 元 严|捐赠 元 覃|捐赠 元 武|捐赠 元 戴|捐赠 元 莫|捐赠 元 孔',
    '捐赠 元 向|捐赠 元 汤|捐赠 元 傅|捐赠 元 阎|捐赠 元 殷|捐赠 元 常|捐赠 元 赖',
    '捐赠 元 康|捐赠 元 施|捐赠 元 牛|捐赠 元 洪',
    '捐赠 元', '慈善']

start = datetime.datetime.now()
log(NOTICE, 'Wechat Crawler Initializing...')
for keyword in keywords:
    wccrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'], SETTINGS['username'], SETTINGS['password'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
