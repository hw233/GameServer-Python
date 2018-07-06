#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import endPointWithoutSocket
import timeU

#代表一个服务节点
class cBackEndEndPoint(endPointWithoutSocket.cEndPointWithoutSocket):
	def __init__(self,*tArgs,**dArgs):#override
		endPointWithoutSocket.cEndPointWithoutSocket.__init__(self,*tArgs,**dArgs)
		self.iCreateStamp=timeU.getStamp()#创建时间

	def _getEP2send(self):#override
		raise NotImplementedError,'请在子类实现.'

if 'mainService' in SYS_ARGV:
	class cEndPoint4ms(cBackEndEndPoint):
		def __init__(self,*tArgs,**dArgs):
			cBackEndEndPoint.__init__(self,*tArgs,**dArgs)

		def _getEP2send(self):#override
			return client4route.getRouteEp4ms()

if 'sceneService' in SYS_ARGV:
	class cEndPoint4ss(cBackEndEndPoint):
		def __init__(self,*tArgs,**dArgs):
			cBackEndEndPoint.__init__(self,*tArgs,**dArgs)

		def _getEP2send(self):#override
			return client4route.getRouteEp4ss()

		def _getPool(self):#override
			return gevent.pool.Pool(50)#协程池,限制最大并发数

if 'fightService' in SYS_ARGV:
	class cEndPoint4fs(cBackEndEndPoint):
		def __init__(self,*tArgs,**dArgs):
			cBackEndEndPoint.__init__(self,*tArgs,**dArgs)

		def _getEP2send(self):#override
			return client4route.getRouteEp4fs()

if 'chatService' in SYS_ARGV:
	class cEndPoint4cs(cBackEndEndPoint):
		def __init__(self,*tArgs,**dArgs):
			cBackEndEndPoint.__init__(self,*tArgs,**dArgs)

		def _getEP2send(self):#override
			return client4route.getRouteEp4cs()


import client4route
import gevent.pool