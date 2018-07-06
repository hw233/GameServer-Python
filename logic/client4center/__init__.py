#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import endPointWithSocket
import backEnd_center_pb2
import client4center.service
import center_collect_pb2
import collect.service4center
import backEnd_pb2

MIN_DELAY,MAX_DELAY = 0.01,3
 
def blockConnect(iBackEndType):#尝试连接,直到成功
	iDelay=MIN_DELAY
	while True:
		#print '后端尝试重连到路由,后端类型=',iBackEndType
		ep=getCenterEndPoint(iBackEndType)#获取时会自动连
		if ep:#连接成功
			return ep
		iDelay = min(MAX_DELAY, iDelay * 2)
		gevent.sleep(iDelay)

class cCenterEndPoint(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,iBackEndType,*tArgs,**dArgs):	
		self.iBackEndType=iBackEndType	
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)

	def _onDisConnected(self):#override
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		sText='与中心服连接断线了.'
		print sText
		log.log('info',sText)
		global gCenterEndPoint
		gCenterEndPoint=None
		# #断线了,要尝试重连.
		#断线了,要尝试重连.启动一个协程里不断地尝试
		myGreenlet.cGreenlet.spawn(blockConnect,self.iBackEndType)

def connect2center(iBackEndType):
	with gLock4createEndPoint:#要加锁,因为创建连接是异步过程
		global gCenterEndPoint
		sIP,iPort=config.CENTER_SERVICE_IP,config.CENTER_PORT
		if gCenterEndPoint:#已建立了连接了
			return

		print ('center client:starting try to connect to ip:{} port:{}'.format(sIP,iPort))
		try:
			sock=gevent.socket.create_connection((sIP,iPort))
		except Exception:
			sText='连接中心服务器失败.ip:{},port:{}'.format(sIP,iPort)
			print sText
			log.log('info',sText)
			return
		sText='连接中心服务器成功.ip:{},port:{}'.format(sIP,iPort)
		print sText
		log.log('info',sText)
		bDebugMode=True
		dProtocol={'service':(	client4center.service.cService,
								collect.service4center.cService,
								),
					'stub':(backEnd_center_pb2.backEnd2center_Stub,
							center_collect_pb2.backEnd2center_Stub,
						)
					}
		centerEndPoint=cCenterEndPoint(iBackEndType,bDebugMode,dProtocol)
		centerEndPoint.setIP(sIP).setPort(iPort).setSocket(sock)
		centerEndPoint.start()

		bFail,uMsg=centerEndPoint.rpcBackEndReport(config.ZONE_NO, iBackEndType, config.ZONE_NAME, config.PAGE_NO)#报告自身身份
		if bFail:
			sText='向中心服务器报到失败.ip:{},port:{},原因:{}'.format(sIP,iPort,uMsg.sReason)
			print sText
			log.log('info',sText)
			return False
		gCenterEndPoint=centerEndPoint
		sText='向中心服务器报到成功.ip:{},port:{}'.format(sIP,iPort)
		log.log('info',sText)
		print sText
		return True

if 'mainService' in SYS_ARGV:
	def getCenterEp4ms():
		return getCenterEndPoint()

if 'chatService' in SYS_ARGV:
	def getCenterEp4ss():
		return getCenterEndPoint(backEnd_pb2.CHAT_SERVICE)

def getCenterEndPoint(iBackEndType=backEnd_pb2.MAIN_SERVICE):#取得ep,没有则连接中心服务器后再返回ep
	if gCenterEndPoint:#大多数是走这里进去了,如果仅有下面的代码每次都加锁,不好
		return gCenterEndPoint

	with gLock4getEndPoint:
		if gCenterEndPoint is None:
			connect2center(iBackEndType)
			# raise Exception,'连接到中心服务器失败'
		return gCenterEndPoint

import socket
import gevent
import gevent.socket
import gevent.lock
import myGreenlet
import u
import log

import config

if 'gbOnce' not in globals():
	gbOnce=True

	if set(['mainService','sceneService','fightService','chatService']) & SYS_ARGV:		
		gCenterEndPoint=None

		gLock4createEndPoint=gevent.lock.RLock()
		gLock4getEndPoint=gevent.lock.RLock()
