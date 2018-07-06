#为了产生core dump文件
ulimit -c unlimited

svn update
if test -e 'service.pid'
then
	pid=`cat service.pid`
	kill -9 $pid
	rm service.pid
fi

nohup python logic/main.py routeService 1 &
nohup python logic/main.py sceneService 1 &
nohup python logic/main.py gateService 1 &
nohup python logic/main.py mainService 1 &
nohup python logic/main.py chatService 1 &

