# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Apr 2, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import os
import sys
from core.google import ggcrawler
from core.log import *
from settings import SETTINGS

current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)


keywords = [
    '捐赠 元 王 OR 李 OR 张 OR 刘 OR 陈 OR 杨 OR 黄 OR 赵 OR 吴 OR 周 OR 徐 OR 孙 OR 马 OR 朱 OR 胡 OR 郭 OR 何 OR 高 OR 林 OR 郑 OR 谢 OR 罗 OR 梁 OR 宋 OR 唐 OR 许 OR 韩 OR 冯 OR 邓 OR 曹',
    '捐赠 元 彭 OR 曾 OR 萧 OR 田 OR 董 OR 袁 OR 潘 OR 于 OR 蒋 OR 蔡 OR 余 OR 杜 OR 叶 OR 程 OR 苏 OR 魏 OR 吕 OR 丁 OR 任 OR 沈 OR 姚 OR 卢 OR 姜 OR 崔 OR 钟 OR 谭 OR 陆 OR 汪 OR 范 OR 金',
    '捐赠 元 石 OR 廖 OR 贾 OR 夏 OR 韦 OR 付 OR 方 OR 白 OR 邹 OR 孟 OR 熊 OR 秦 OR 邱 OR 江 OR 尹 OR 薛 OR 闫 OR 段 OR 雷 OR 侯 OR 龙 OR 史 OR 陶 OR 黎 OR 贺 OR 顾 OR 毛 OR 郝 OR 龚 OR 邵',
    '捐赠 元 万 OR 钱 OR 严 OR 覃 OR 武 OR 戴 OR 莫 OR 孔 OR 向 OR 汤 OR 傅 OR 阎 OR 殷 OR 常 OR 赖 OR 康 OR 施 OR 牛 OR 洪'
]

start = datetime.datetime.now()
log(NOTICE, 'Google Crawler Initializing...')
for keyword in keywords:
    ggcrawler(keyword, SETTINGS['project'], SETTINGS['address'], SETTINGS['port'], SETTINGS['username'], SETTINGS['password'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
