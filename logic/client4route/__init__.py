#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import config
import client
import backEnd_route_pb2
import bridgeEndPoint

import p
CONN_ID_SIZE=4 #连接id的大小
CONN_ID_COMMAND=0

MIN_DELAY,MAX_DELAY = 0.01,3
 
def blockConnect(iBackEndType):#尝试连接,直到成功
	iDelay=MIN_DELAY
	while True:
		#print '后端尝试重连到路由,后端类型=',iBackEndType
		log.log('info','尝试连到route')
		ep=_getRouteEndPoint(iBackEndType)#获取时会自动连
		if ep:#连接成功
			log.log('info','连接route成功')
			return ep
		iDelay = min(MAX_DELAY, iDelay * 2)
		gevent.sleep(iDelay)

class cRouteEndPoint(bridgeEndPoint.cBridgeEndPoint):
	def __init__(self,iBackEndType,*tArgs,**dArgs):
		self.iBackEndType=iBackEndType
		bridgeEndPoint.cBridgeEndPoint.__init__(self,*tArgs,**dArgs)

	def _onDisConnected(self):#override
		bridgeEndPoint.cBridgeEndPoint._onDisConnected(self)
		sText='与路由服{}:{}的连接断线了.'.format(self.ip(),self.iPort)
		print sText
		log.log('info',sText)
		global gRouteEndPoint
		gRouteEndPoint=None
		#断线了,要尝试重连.启动一个协程里不断地尝试
		myGreenlet.cGreenlet.spawn(blockConnect,self.iBackEndType)

	def interceptAndDeal(self,sPacket):#override 是否拦截并处理
		sConnId,sNewPacket=sPacket[:CONN_ID_SIZE],sPacket[CONN_ID_SIZE:]
		iFrom=p.cUnPack(sConnId).unPackInt(CONN_ID_SIZE)
		if iFrom==CONN_ID_COMMAND:
			return False,sNewPacket
		self._dispatch2backEnd(iFrom,sNewPacket)
		return True,sNewPacket

	def _getGameClientEP(self,iFrom):
		raise NotImplementedError,'请在子类实现.'

	def _dispatch2backEnd(self,iFrom,sPacket):
		raise NotImplementedError,'请在子类实现.'

if 'mainService' in SYS_ARGV:
	class cRouteEP4ms(cRouteEndPoint):
		def _dispatch2backEnd(self,iFrom,sPacket):#override
			if iFrom==backEnd_pb2.MAIN_SERVICE:
				raise Exception,'不可能{}'.format(iFrom)
			if iFrom==backEnd_pb2.SCENE_SERVICE:
				backEnd.gSceneEp4ms.recvPacket(sPacket)
			elif iFrom==backEnd_pb2.FIGHT_SERVICE:
				backEnd.gFightEp4ms.recvPacket(sPacket)
			elif iFrom==backEnd_pb2.CHAT_SERVICE:
				backEnd.gChatEp4ms.recvPacket(sPacket)
			else:
				raise Exception,'未知的数据来源'

		def _getGameClientEP(self,iFrom):#override
			return mainService.gEndPointKeeper.getObj(iFrom)

if 'sceneService' in SYS_ARGV:
	class cRouteEP4ss(cRouteEndPoint):
		def _dispatch2backEnd(self,iFrom,sPacket):#override
			if iFrom==backEnd_pb2.SCENE_SERVICE:
				raise Exception,'不可能{}'.format(iFrom)
			if iFrom==backEnd_pb2.MAIN_SERVICE:
				backEnd.gMainEp4ss.recvPacket(sPacket)
			elif iFrom==backEnd_pb2.FIGHT_SERVICE:
				backEnd.gFightEp4sceneEp.recvPacket(sPacket)
			else:
				raise Exception,'未知的数据来源'

if 'fightService' in SYS_ARGV:
	class cRouteEP4fs(cRouteEndPoint):
		def _dispatch2backEnd(self,iFrom,sPacket):#override
			if iFrom==backEnd_pb2.FIGHT_SERVICE:
				raise Exception,'不可能{}'.format(iFrom)
			if iFrom==backEnd_pb2.MAIN_SERVICE:
				backEnd.gMainEp4fs.recvPacket(sPacket)
			elif iFrom==backEnd_pb2.SCENE_SERVICE:
				backEnd.gSceneEp4fightEp.recvPacket(sPacket)
			else:
				raise Exception,'未知的数据来源'

if 'chatService' in SYS_ARGV:
	class cRouteEP4cs(cRouteEndPoint):
		def _dispatch2backEnd(self,iFrom,sPacket):#override
			if iFrom==backEnd_pb2.CHAT_SERVICE:
				raise Exception,'不可能{}'.format(iFrom)
			if iFrom==backEnd_pb2.MAIN_SERVICE:
				backEnd.gMainEp4cs.recvPacket(sPacket)
			elif iFrom==backEnd_pb2.SCENE_SERVICE:
				backEnd.gSceneEp4cs.recvPacket(sPacket)
			else:
				raise Exception,'未知的数据来源'
				
		def _getGameClientEP(self,iFrom):#override
			return chatService.gEndPointKeeper.getObj(iFrom)

def connect2route(iBackEndType):#连接至路由
	#print 'connect2route ... connect2route'
	global gRouteEndPoint
	with gLock4createEndPoint:#要加锁,因为创建连接是异步过程	
		if gRouteEndPoint is not None:#已建立了连接了
			return True	
		sIP,iPort=config.ROUTE_SERVICE_IP,config.ROUTE_PORT_FOR_BACK_END

		print ('route client:starting try to connect to ip:{} port:{}'.format(sIP,iPort))
		try:
			sock=gevent.socket.create_connection((sIP,iPort))
		except Exception:
			sText='连接路由服务器失败.ip:{},port:{}'.format(sIP,iPort)
			print sText
			log.log('info',sText)
			return False
		sText='连接路由服务{}:{}成功'.format(sIP,iPort)
		print sText
		log.log('info',sText)

		bDebugMode=True
		if iBackEndType==backEnd_pb2.MAIN_SERVICE:
			cls=cRouteEP4ms
		elif iBackEndType==backEnd_pb2.SCENE_SERVICE:
			cls=cRouteEP4ss
		elif iBackEndType==backEnd_pb2.FIGHT_SERVICE:
			cls=cRouteEP4fs
		elif iBackEndType==backEnd_pb2.CHAT_SERVICE:
			cls=cRouteEP4cs
		else:
			raise Exception,'未知后端类型.'
		dProtocol={'service':(service4route.cService,),'stub':(backEnd_route_pb2.backEnd2route_Stub,)}
		routeEndPoint=cls(iBackEndType,bDebugMode,dProtocol)
		routeEndPoint.setIP(sIP).setPort(iPort).setSocket(sock)
		routeEndPoint.start()
		bFail,uMsg=routeEndPoint.rpcBackEndReport(iBackEndType)#报告自身身份
		if bFail:
			sText='后端向路由报到,rpcBackEndReport失败.{}'.format(uMsg.sReason)
			print sText
			log.log('info',sText)
			return False
		
		gRouteEndPoint=routeEndPoint
		sText='后端向路由{}:{}报到成功'.format(sIP,iPort)
		print sText
		log.log('info',sText)
		return True

# def _notify(iHasReportBitMap):
# 	iBackEnd=iHasReportBitMap&backEnd_pb2.MAIN_SERVICE
# 	if iBackEnd!=0:
# 		backEnd.channelBuilt(iBackEnd)

# 	iBackEnd=iHasReportBitMap&backEnd_pb2.SCENE_SERVICE
# 	if iBackEnd!=0:
# 		backEnd.channelBuilt(iBackEnd)

# 	iBackEnd=iHasReportBitMap&backEnd_pb2.FIGHT_SERVICE
# 	if iBackEnd!=0:
# 		backEnd.channelBuilt(iBackEnd)

# 	iBackEnd=iHasReportBitMap&backEnd_pb2.CHAT_SERVICE
# 	if iBackEnd!=0:
# 		backEnd.channelBuilt(iBackEnd)

if 'mainService' in SYS_ARGV:
	def getRouteEp4ms():	
		return _getRouteEndPoint(backEnd_pb2.MAIN_SERVICE)

if 'sceneService' in SYS_ARGV:
	def getRouteEp4ss():
		return _getRouteEndPoint(backEnd_pb2.SCENE_SERVICE)

if 'fightService' in SYS_ARGV:
	def getRouteEp4fs():
		return _getRouteEndPoint(backEnd_pb2.FIGHT_SERVICE)

if 'chatService' in SYS_ARGV:
	def getRouteEp4cs():
		return _getRouteEndPoint(backEnd_pb2.CHAT_SERVICE)


def _getRouteEndPoint(iBackEndType):#取得ep,没有则连接路由服务器后再返回ep
	if gRouteEndPoint is not None:#大多数是走这里就返回了,如果仅有下面的代码,则会每次都加锁,不好
		return gRouteEndPoint

	with gLock4getEndPoint:
		if gRouteEndPoint is None:
			connect2route(iBackEndType)#连接1次,有可能是不成功的,特别是路由宕掉后		
		return gRouteEndPoint

import platform
import socket
import traceback
import gevent
import gevent.socket
import gevent.lock


import misc
import u
import log
import myGreenlet

#import config_pb2
import mainService
import chatService
import config
import backEnd
import backEnd_pb2
import routeService
import service4route

if 'gbOnce' not in globals():
	gbOnce=True

	if set(['mainService','sceneService','fightService','chatService']) & SYS_ARGV:				
		gRouteEndPoint=None #路由endpoint
		gLock4createEndPoint=gevent.lock.RLock()
		gLock4getEndPoint=gevent.lock.RLock()
