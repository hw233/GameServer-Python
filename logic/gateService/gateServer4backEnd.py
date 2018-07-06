#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import config
import backEnd_gate_pb2
import gateService4backEnd
import gateService

import bridgeEndPoint

class cBackEndEndPoint(bridgeEndPoint.cBridgeEndPoint):
	def __init__(self,*tArgs,**dArgs):
		bridgeEndPoint.cBridgeEndPoint.__init__(self,*tArgs,**dArgs)
		self.iBackEndType=backEnd_pb2.UNKNOWN_SERVICE

	def setBackEndType(self,iBackEndType):
		self.iBackEndType=iBackEndType

	def interceptAndDeal(self,sPacket):#override 收到包是否拦截并处理
		mPacket=memoryview(sPacket)
		mConnId,mNewPacket=mPacket[:gateService.CONN_ID_SIZE],mPacket[gateService.CONN_ID_SIZE:]
		iTarget=p.cUnPack(mConnId).unPackInt(gateService.CONN_ID_SIZE)
		if iTarget==gateService.CONN_ID_COMMAND:#控制命令
			return False,mNewPacket.tobytes()
		#去掉连接id头之后,剩下的发给游戏客户端
		oClientConn=server4gameClient.gConnKeeper.getObj(iTarget)
		if oClientConn:
			oClientConn.send(self.iBackEndType,mNewPacket)
			
			if self.iBackEndType==backEnd_pb2.MAIN_SERVICE:#如果是主服务ep,额外处理一段逻辑
				dealSwitchScene(mNewPacket.tobytes(),iTarget)
		else:
			print '网关从backEnd收到包往{}客户端发,但是客户端不存在'.format(iTarget)
		return True,mNewPacket #返回True时,第2个元素是要丢弃掉的

	def _onDisConnected(self):#override
		sText='与{}的连接断开了'.format(backEnd.gdServiceName[self.iBackEndType])
		print sText
		log.log('connection4backEnd',sText)#记log
		bridgeEndPoint.cBridgeEndPoint._onDisConnected(self)
		#后端与网关之间的连接断了,应该把游戏客户端与网关之间的连接也断掉
		#后端改为可单独重启，不用关闭了
		# for ep in server4gameClient.gConnKeeper.getValues():
		# 	ep.shutdown()

def dealSwitchScene(sBuffer,iTarget):
	packet=universal.public_pb2.packet()
	packet.ParseFromString(sBuffer)
	if packet.iType==universal.public_pb2.TYPE_REQUEST:
		req=universal.public_pb2.request()
		req.ParseFromString(packet.sSerialized)
		if req.sMethodName=='rpcSwitchScene':
			oMainBackEnd = gBackEndProxy.getProxy(1)
			if not oMainBackEnd:
				return
			oMainBackEnd.rpcSwitchSceneResponse(iTarget)



def nextEndPointId():
	global giEndPointId
	if 'giEndPointId' not in globals():
		giEndPointId=0
	giEndPointId+=1
	return giEndPointId


def afterAccept(oSocket,tAddress,iGateServiceId,iListenPort):
	sIP,iPort=tAddress
	#这里可以控制总连接数sock.shutdown()
	print 'gate service listen {} for back end:new connection from ip:{} port:{}'.format(iListenPort,sIP,iPort)	
	log.log('connection4backEnd','我方监听端口:{},收到连接ip:{} port:{}'.format(iListenPort,sIP,iPort))#记log

	bDebugMode=config.IS_INNER_SERVER
	dProtocol={'service':(gateService4backEnd.cService,),'stub':(backEnd_gate_pb2.gate2backEnd_Stub,)}
	ep=cBackEndEndPoint(bDebugMode,dProtocol)
	ep.setEndPointId(nextEndPointId())
	ep.setIP(sIP).setPort(iPort).setSocket(oSocket)
	ep.start()

	ep.join()

def initServer(iGateServiceId=1):
	iListenPort=config.GATE_PORT_FOR_BACK_END
	oServer=gevent.server.StreamServer(('127.0.0.1',iListenPort),u.cFunctor(afterAccept,iGateServiceId,iListenPort))
	print ('starting gate server for back end on port {}'.format(iListenPort))
	return oServer

import keeper
import u

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'gateService' in SYS_ARGV:
		gBackEndKeeper=keeper.cKeeper()#连接id 映射 连接对象

		gBackEndProxy=u.cKeyMapProxy()

import traceback
import gevent
import gevent.socket
import gevent.queue	
import gevent
import gevent.server
import gevent.queue
import gevent.core
import universal.public_pb2
import backEnd_pb2
import config

import c
import p
import misc
import log
import timeU
import timer
import server4gameClient
import backEnd