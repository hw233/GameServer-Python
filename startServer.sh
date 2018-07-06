#!/bin/sh
shPath=$PWD"//"
cd logic
nohup python main.py mainService $shPath >/dev/null &
#python main.py mainService $shPath
