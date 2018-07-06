#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import config
import client
import backEnd_gate_pb2
import bridgeEndPoint

import p
CONN_ID_SIZE=4 #连接id的大小

CONN_ID_COMMAND=0


MIN_DELAY,MAX_DELAY = 0.01,3
 
def blockConnect(iBackEndType,iGateServiceNo):#尝试连接,直到成功
	iDelay=MIN_DELAY
	while True:
		#print '后端尝试重连到网关,后端类型=',iBackEndType
		ep=_getGateEndPoint(iBackEndType,iGateServiceNo)#获取时会自动连
		if ep:#连接成功
			return ep
		iDelay = min(MAX_DELAY, iDelay * 2)
		gevent.sleep(iDelay)

class cGateEndPoint(bridgeEndPoint.cBridgeEndPoint):
	def __init__(self,iBackEndType,iGateServiceNo,*tArgs,**dArgs):
		self.iBackEndType=iBackEndType
		self.iGateServiceNo=iGateServiceNo
		bridgeEndPoint.cBridgeEndPoint.__init__(self,*tArgs,**dArgs)

	def gateServiceNo(self):
		return self.iGateServiceNo

	def _onDisConnected(self):#override
		bridgeEndPoint.cBridgeEndPoint._onDisConnected(self)
		sText='与{}号网关服{}:{}的连接断线了.'.format(self.iGateServiceNo,self.ip(),self.iPort)
		print sText
		log.log('info',sText)
		gdGateEndPoint.pop(self.iGateServiceNo,None)

		#断线了,要尝试重连.启动一个协程里不断地尝试
		myGreenlet.cGreenlet.spawn(blockConnect,self.iBackEndType,self.iGateServiceNo)

	def interceptAndDeal(self,sPacket):#override 是否拦截并处理
		sConnId,sNewPacket=sPacket[:CONN_ID_SIZE],sPacket[CONN_ID_SIZE:]
		iFrom=p.cUnPack(sConnId).unPackInt(CONN_ID_SIZE)
		if iFrom==CONN_ID_COMMAND:
			return False,sNewPacket
		ep=self._getGameClientEP(iFrom)
		if ep:
			ep.recvPacket(sNewPacket)
		else:
			print 'id为{}的游戏客户端end point不存在.'.format(iFrom)
		return True,sNewPacket

	def _getGameClientEP(self,iFrom):
		raise NotImplementedError,'请在子类实现.'

if 'mainService' in SYS_ARGV:
	class cGateEP4ms(cGateEndPoint):
		def _getGameClientEP(self,iFrom):#override
			return mainService.gEndPointKeeper.getObj(iFrom)

if 'sceneService' in SYS_ARGV:
	class cGateEP4ss(cGateEndPoint):
		def _getGameClientEP(self,iFrom):#override
			return sceneService.gEndPointKeeper.getObj(iFrom)

if 'fightService' in SYS_ARGV:
	class cGateEP4fs(cGateEndPoint):
		pass

if 'chatService' in SYS_ARGV:
	class cGateEP4cs(cGateEndPoint):
		def _getGameClientEP(self,iFrom):#override
			return chatService.gEndPointKeeper.getObj(iFrom)

def connect2gate(iBackEndType):#连接至网关,可能有多个网关
	with gLock4createEndPoint:#要加锁,因为创建连接是异步过程
		for info in [(1,config.GATE_SERVICE_IP,config.GATE_PORT_FOR_BACK_END)]:
			#iGateServiceNo,sIP,iPort=info.iGateServiceNo,info.sIP,info.iPort	
			iGateServiceNo,sIP,iPort=info
			if iGateServiceNo in gdGateEndPoint:#已建立了连接了
				continue

			print ('gate client:starting try to connect to ip:{} port:{}'.format(sIP,iPort))
			try:
				sock=gevent.socket.create_connection((sIP,iPort))
			except Exception:
				sText='连接网关服务器失败.ip:{},port:{}'.format(sIP,iPort)
				print sText
				log.log('info',sText)
				return False
			sText='连接{}号网关服{}:{}成功'.format(iGateServiceNo,sIP,iPort)
			print sText
			log.log('info',sText)

			bDebugMode=True
			if iBackEndType==backEnd_pb2.MAIN_SERVICE:
				cls=cGateEP4ms
			elif iBackEndType==backEnd_pb2.SCENE_SERVICE:
				cls=cGateEP4ss
			elif iBackEndType==backEnd_pb2.FIGHT_SERVICE:
				cls=cGateEP4fs
			elif iBackEndType==backEnd_pb2.CHAT_SERVICE:
				cls=cGateEP4cs
			else:
				raise Exception,'未知后端类型.'
			dProtocol={'service':(service4gate.cService,),'stub':(backEnd_gate_pb2.backEnd2gate_Stub,)}
			gateEndPoint=cls(iBackEndType,iGateServiceNo,bDebugMode,dProtocol)
			gateEndPoint.setIP(sIP).setPort(iPort).setSocket(sock)
			gateEndPoint.start()
			bFail,uMsg=gateEndPoint.rpcBackEndReport(iBackEndType)#报告自身身份
			if bFail:
				sText='后端向网关报到,rpcBackEndReport失败.{}'.format(uMsg.sReason)
				print sText
				log.log('info',sText)
				return False
			gdGateEndPoint[iGateServiceNo]=gateEndPoint
			sText='向{}号网关服{}:{}报到成功'.format(iGateServiceNo,sIP,iPort)
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
	def getGateEp4ms(iGateServiceNo=1):	
		return _getGateEndPoint(backEnd_pb2.MAIN_SERVICE,iGateServiceNo)

if 'sceneService' in SYS_ARGV:
	def getGateEp4ss(iGateServiceNo=1):
		return _getGateEndPoint(backEnd_pb2.SCENE_SERVICE,iGateServiceNo)

if 'fightService' in SYS_ARGV:
	def getGateEp4fs(iGateServiceNo=1):
		return _getGateEndPoint(backEnd_pb2.FIGHT_SERVICE,iGateServiceNo)

if 'chatService' in SYS_ARGV:
	def getGateEp4cs(iGateServiceNo=1):
		return _getGateEndPoint(backEnd_pb2.CHAT_SERVICE,iGateServiceNo)


def _getGateEndPoint(iBackEndType,iGateServiceNo=1):#取得ep,没有则连接网关服务器后再返回ep
	if iGateServiceNo==0:
		raise Exception,'参数不可以是0'

	if iGateServiceNo in gdGateEndPoint:#大多数是走这里就返回了,如果仅有下面的代码,则会每次都加锁,不好
		return gdGateEndPoint[iGateServiceNo]

	with gLock4getEndPoint:
		if iGateServiceNo not in gdGateEndPoint:
			connect2gate(iBackEndType)#连接1次,有可能是不成功的,特别是网关宕掉后
			#if iGateServiceNo not in gdGateEndPoint:
			#	raise Exception,'没有{}号网关服务'.format(iGateServiceNo)
		return gdGateEndPoint.get(iGateServiceNo)

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
import sceneService
import config
import backEnd
import backEnd_pb2
import gateService
import service4gate

if 'gbOnce' not in globals():
	gbOnce=True

	if set(['mainService','sceneService','fightService','chatService']) & SYS_ARGV:		
		gdGateEndPoint={} #网关服channel,假设有多个网关服

		gLock4createEndPoint=gevent.lock.RLock()
		gLock4getEndPoint=gevent.lock.RLock()
