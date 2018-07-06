#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import config
import backEnd_route_pb2
import routeService4backEnd
import endPointWithSocket
import routeService
import gateService
import backEnd_pb2
import p
import bridgeEndPoint

SERIALIZED_MAIN=p.cPack().packInt(routeService.CONN_ID_SIZE,backEnd_pb2.MAIN_SERVICE).getBuffer()
SERIALIZED_SCENE=p.cPack().packInt(routeService.CONN_ID_SIZE,backEnd_pb2.SCENE_SERVICE).getBuffer()
SERIALIZED_FIGHT=p.cPack().packInt(routeService.CONN_ID_SIZE,backEnd_pb2.FIGHT_SERVICE).getBuffer()
SERIALIZED_CHAT=p.cPack().packInt(routeService.CONN_ID_SIZE,backEnd_pb2.CHAT_SERVICE).getBuffer()

gdNoMapSerialized={
	backEnd_pb2.UNKNOWN_SERVICE:routeService.SERIALIZED_UNKNOWN,
	backEnd_pb2.MAIN_SERVICE:SERIALIZED_MAIN,
	backEnd_pb2.SCENE_SERVICE:SERIALIZED_SCENE,
	backEnd_pb2.FIGHT_SERVICE:SERIALIZED_FIGHT,
	backEnd_pb2.CHAT_SERVICE:SERIALIZED_CHAT,
}

class cBackEndEndPoint(bridgeEndPoint.cBridgeEndPoint):
	def __init__(self,*tArgs,**dArgs):
		bridgeEndPoint.cBridgeEndPoint.__init__(self,*tArgs,**dArgs)
		self.iBackEndType=backEnd_pb2.UNKNOWN_SERVICE

	def setBackEndType(self,iBackEndType):
		self.iBackEndType=iBackEndType

	def interceptAndDeal(self,sPacket):#override 收到包是否拦截并处理
		mPacket=memoryview(sPacket)
		mConnId,mNewPacket=mPacket[:routeService.CONN_ID_SIZE],mPacket[routeService.CONN_ID_SIZE:]
		iTarget=p.cUnPack(mConnId).unPackInt(routeService.CONN_ID_SIZE)
		if iTarget==routeService.CONN_ID_COMMAND:#控制命令
			return False,mNewPacket.tobytes()

		if self.iBackEndType==backEnd_pb2.UNKNOWN_SERVICE:
			raise Exception,'尚未清楚自身类型.'

		backEndEP=gBackEndProxy.getProxy(iTarget)
		if backEndEP:
			sFrom=gdNoMapSerialized[self.iBackEndType]
			backEndEP.send(mNewPacket,sFrom)#包头原来是target,转发后要换成from
		else:
			#只是打印下,方便调试
			sNewPacket=mNewPacket.tobytes()
			packet=universal.public_pb2.packet()
			packet.ParseFromString(sNewPacket)
			if packet.iType==universal.public_pb2.TYPE_REQUEST:
				req=universal.public_pb2.request()
				req.ParseFromString(packet.sSerialized)
				sWhat=req.sMethodName
			else:
				sWhat='是一个回应包'

			sServiceName=backEnd.gdServiceName[iTarget]
			print 'iTarget={}的{}不存在,包内容:{}'.format(iTarget,sServiceName,sWhat)
		return True,mNewPacket #返回True时,第2个元素是要丢弃掉的

	def _onDisConnected(self):#override
		sText='与{}的连接断开了'.format(backEnd.gdServiceName[self.iBackEndType])
		print sText
		log.log('connection4backEnd',sText)#记log
		bridgeEndPoint.cBridgeEndPoint._onDisConnected(self)

		#后端与路由之间的连接断了,应该把游戏客户端与路由之间的连接也断掉
		# for ep in server4gameClient.gConnKeeper.getValues():
		# 	ep.shutdown()


def nextEndPointId():
	global giEndPointId
	if 'giEndPointId' not in globals():
		giEndPointId=0
	giEndPointId+=1
	return giEndPointId


def afterAccept(oSocket,tAddress,iListenPort):
	sIP,iPort=tAddress
	#这里可以控制总连接数sock.shutdown()
	print 'route service listen {} for back end:new connection from ip:{} port:{}'.format(iListenPort,sIP,iPort)	
	log.log('connection4backEnd','我方监听端口:{},收到连接ip:{} port:{}'.format(iListenPort,sIP,iPort))#记log

	bDebugMode=config.IS_INNER_SERVER
	dProtocol={'service':(routeService4backEnd.cService,),'stub':(backEnd_route_pb2.route2backEnd_Stub,)}
	ep=cBackEndEndPoint(bDebugMode,dProtocol)
	ep.setEndPointId(nextEndPointId())
	ep.setIP(sIP).setPort(iPort).setSocket(oSocket)
	ep.start()

	ep.join()

def initServer():
	iListenPort=config.ROUTE_PORT_FOR_BACK_END
	oServer=gevent.server.StreamServer(('127.0.0.1',iListenPort),u.cFunctor(afterAccept,iListenPort))
	print ('starting route server for back end on port {}'.format(iListenPort))
	return oServer

import keeper
import u

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'routeService' in SYS_ARGV:
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

import config
import backEnd

import c
import p
import misc
import log
import timeU
import timer
