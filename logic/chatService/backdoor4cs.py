#-*- coding:UTF-8 -*-

def initServer():
	iPort = config.CHAT_BACKDOOR_PORT
	oServer=cBackdoorServer(('0.0.0.0',iPort))
	print ('starting chat backdoor server on port {}'.format(iPort))
	return oServer

import gevent.backdoor

class cBackdoorServer(gevent.backdoor.BackdoorServer):
	pass
# 	def handle(self, conn, address):#override
# 		cSocketConsole.spawn(self.locals, conn, banner=self.banner)

# class cSocketConsole(gevent.backdoor.SocketConsole):
# 	 def __init__(self, locals, conn, banner=None):#override
# 	 	gevent.backdoor.SocketConsole.__init__(self, locals, conn, banner)
# 	 	self.desc = cFileobject(conn) #再次赋值

# class cFileobject(gevent.backdoor._fileobject):
# 	def write(self, data):#override
# 		if platform.system().upper()=="WINDOWS":
# 			data=data.replace('\n','\r\n')
# 		return gevent.backdoor._fileobject.write(self, data)

import gevent.socket
import misc
import config
import platform
