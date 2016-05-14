#!/bin/sh
# free_mememory.sh
# philanthropy data collection program
# Oct. 22, 2015
# Harvard Kennedy School
# Bo Zhao
# bo_zhao@hks.harvard.edu
sudo rm /home/ubuntu/ashcrawler/crawler.log
echo "the daily log has been deleted"
cd /home/ubuntu/ashcrawler/
git checkout --force
git pull
echo "the program has updated to the latest version"
