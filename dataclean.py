# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Jun 3, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


import os
import sys
from settings import SETTINGS
from core.utils import del_duplicates, add_tags


current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(current_path)

del_duplicates(SETTINGS)
add_tags(SETTINGS)

if __name__ == '__main__':
    pass
