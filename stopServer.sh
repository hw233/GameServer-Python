#!/bin/sh
shPath=$PWD"//"
PIDS=`ps -ef | grep -v grep | grep python | grep mainService | grep $shPath | awk '{print $2}'`

#echo "Notify process $PIDS to stop service..."
for PID in $PIDS
do
	#kill -USR2 $PID
	kill -15 $PID
	echo $PID killed
done