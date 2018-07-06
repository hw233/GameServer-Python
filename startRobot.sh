svn update
robotCount=$1
if test -e 'robot.pid'
then
	pid=`cat robot.pid`
	kill -9 $pid
	rm robot.pid
fi

nohup python logic/main.py robot ${robotCount} &

