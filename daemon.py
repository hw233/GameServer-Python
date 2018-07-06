#-*-coding:utf-8-*-
#作者：guicheng.liao

import sys
import os
import time
import atexit 
import string
import signal


class cDaemon(object):
	def __init__(self,pidfile,stdin='/dev/null',stdout='/dev/null',stderr='/dev/null'):
		self.stdin=stdin
		self.stdout=stdout
		self.stderr=stderr
		self.pidfile=pidfile

	def _daemonize(self):
		try:
			pid=os.fork()
			if pid>0:
				sys.exit(0)
		except OSError,e:
			sys.stderr.write('fork #1 failed: %d(%s)\n' % (e.errno,e.strerror))
			sys.exit(1)
		sys.stdout.flush()
		sys.stderr.flush()
		si=file(self.stdin,'r')
		so=file(self.stdout,'a+')
		se=file(self.stderr,'a+',0)
		os.dup2(si.fileno(),sys.stdin.fileno())
		os.dup2(so.fileno(),sys.stdout.fileno())
		os.dup2(se.fileno(),sys.stderr.fileno())

		#创建processid文件
		atexit.register(self.delpid)
		pid=str(os.getpid())
		fp=file(self.pidfile,'w+')
		fp.write('%s\n' % pid)
		fp.close()
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		try:
			pf=file(self.pidfile,'r')
			pid=int(pf.read().strip())
			pf.close()
		except IOError:
			pid=None
		
		if pid:
			message='pidfile %s already exit. Daemon already running?\n'
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)

		#启动监控
		self._daemonize()
		self._run()

	def stop(self):
		try:
			pf=file(self.pidfile,'r')
			pid=int(pf.read().strip())
			pf.close()
		except IOError:
			pid=None
			
		if pid:
			try:
				while True:
					os.kill(pid, signal.SIGTERM)
					time.sleep(0.1)
					#os.system('echo "你想停止的程序"')
			except OSError,err:
				err=str(err)
				if err.find('No such process') > 0:
					if os.path.exists(self.pidfile):
						os.remove(self.pidfile)
		
		# lSvPid=os.popen('ps -ef | grep "python" | grep -v "grep" | grep -v daemon.py | grep "mainServer" | awk \'{print $2}\'').read().strip().split('\n')
		# if not lSvPid or not lSvPid[0]:
		# 	return
		
		# try:#杀死python main.py mainServer
		# 	while True:
		# 		os.kill(lSvPid[0], signal.SIGTERM)
		# 		time.sleep(0.1)
		# 		#os.system('echo "你想停止的程序"')
		# except OSError,err:
		# 	pass

	def restart(self):
		self.stop()
		self.start()

	def _run(self):
		while True:
			apollo=os.popen('ps -ef | grep "python" | grep "main.py" | grep "sceneService" | grep -v "grep" | wc -l').read().strip()
			if apollo=='0':
				os.system('nohup python logic/main.py sceneService > /dev/null 2>&1 &')
			time.sleep(2)


if __name__=='__main__':
	daemon=cDaemon('watch_process.pid')
	if len(sys.argv)==2:
		if 'start'==sys.argv[1]:
			daemon.start()
		elif 'stop'==sys.argv[1]:
			daemon.stop()
		elif 'restart'==sys.argv[1]:
			daemon.restart()
		else:
			print 'Unknown command'
			sys.exit(2)
	else:
		print 'usage: %s start|stop|resart' % sys.argv[0]
		sys.exit(2)
