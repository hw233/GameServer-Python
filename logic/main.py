#!/usr/bin/python
#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#请不要在这个模块写代码
#要往init.py中写初始化代码
class PlannerError(Exception):
	pass


def writePID():
	import os
	
	if 'centerService' in SYS_ARGV:
		return
	
	pidFileName = "service.pid"
	if 'robot' in SYS_ARGV:
		pidFileName = "robot.pid"
	
	pid = os.getpid()
	print "pid:", pid
	f = open(pidFileName, "a")
	f.write("%s\n" % pid)
	f.close()


#__builtins__在linux下是dict,在windows下是module,奇葩
if __name__ == '__main__':
	import types
	if type(__builtins__)==types.DictType:
		__builtins__["PlannerError"] = PlannerError
	else:
		__builtins__.PlannerError=PlannerError

	try:
		#import gevent
		import sys
		if type(__builtins__)==types.DictType:
			__builtins__["SYS_ARGV"] = set(sys.argv)
		else:
			__builtins__.SYS_ARGV=set(sys.argv)
		print 'sys.argv==',sys.argv
		writePID()
		import init#这个import的上面不能有其他import,主要是防止间接import了traceback
		
		init.start(sys.argv)
	except Exception:
		try:			
			import os
			import sys
			import platform
			import traceback
			#print traceback #看是否正确地导入了修改后的traceback
			sText=traceback.format_exc()
			sys.stderr.write(sText)			
	
			import u
			import log 
			log.closeAll()
			
		except Exception:			
			traceback.print_exc(None,sys.stdout)

		if platform.system().upper()=="WINDOWS":
			os.system(u.trans('echo 系统发生异常,请查看log'))
			os.system('pause')
			print '======================================================='
			#os.system('startMainServer.bat')
			#os.system('cd logic')
			#os.system('start logic/main.py mainServer')
		else:#linux
			pass


