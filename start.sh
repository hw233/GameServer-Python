#!/bin/sh
#服务由sh启动,定义该用户的环境变量。
#别忘了第一行必须是：
#!/bin/sh

cd `dirname $0` #进入工作目录，dirname $0获得脚本所在路径
svn update
if test -e 'watch_process.pid'
then
	pid=`cat watch_process.pid`
	kill -9 $pid
	rm watch_process.pid
fi
python daemon.py start #开启服务，并且守护服务进程，一旦挂掉，马上重启服务
