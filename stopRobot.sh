if test -e 'robot.pid'
then
	pid=`cat robot.pid`
	kill -9 $pid
	rm robot.pid
fi

