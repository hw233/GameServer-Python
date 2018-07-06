#-*- coding:UTF-8 -*-

def initServer():	
	iPort=config.BACKDOOR_PORT
	oServer=cBackdoorServer(('0.0.0.0',iPort))
	print ('starting backdoor server on port {}'.format(iPort))
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
# 	#def readline(self, *a):#override
# 	#	return gevent.socket._fileobject.readline(self, *a) #.replace("\r\n", "\n")	
	
# 	def write(self, data):#override
# 		data=data.replace('\n','\r\n')
# 		return gevent.backdoor._fileobject.write(self, data)

import gevent.socket
import misc
import config