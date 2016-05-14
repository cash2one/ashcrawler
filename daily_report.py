# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

# Important: Before deploying the program, compare the deploying version with
# a normal debugging version, especially checkking which path is not loaded in
# sys.path. Other than the root of the program, I noticed that another path as
# show below is not attached as well. (I cost almost 24 hours to find it out..)

import sys
import os
from core.report import brief_report
from settings import SETTINGS

current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)

brief_report(SETTINGS)

if __name__ == '__main__':
    pass
