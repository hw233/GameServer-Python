#! /bin/bash
svn add --force *.py
svn commit -m "commit planner data on linux" >commit.result && cd data && sh commit.sh && cd ..
