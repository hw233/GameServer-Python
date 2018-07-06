#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import backEnd_center_pb2
import centerService.service
import center_collect_pb2
import collect.service4main
import endPointWithSocket

class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,*tArgs,**dArgs):
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)
		self.iZoneNo = 0
		self.iBackEndType = 0
		self.sZoneName = ""
		self.iPageNo = 0

	def _onDisConnected(self):#override
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		print '一个backEnd连接断开了'
		gBackEndKeeper.removeObj(self.iEndPointId)
		gBackEndProxy.removeProxy((self.iZoneNo, self.iBackEndType))
		self.iZoneNo = 0
		self.iBackEndType = 0

	def setAssociative(self, iZoneNo, iBackEndType, sZoneName, iPageNo):
		self.iZoneNo = iZoneNo
		self.iBackEndType = iBackEndType
		self.sZoneName = sZoneName
		self.iPageNo = iPageNo
		gBackEndProxy.addObj(self, (self.iZoneNo, self.iBackEndType))


def nextEndPointId():
	global giEndPointId
	if 'giEndPointId' not in globals():
		giEndPointId=0
	giEndPointId+=1
	return giEndPointId


def afterAccept(oSocket,tAddress,iListenPort):
	sIP,iPort=tAddress
	#这里可以控制总连接数sock.shutdown()
	print '一个backEnd连接 ip:{} port:{}'.format(sIP,iPort)
	log.log('connection','ip:{} port:{}'.format(sIP,iPort))#记log

	bDebugMode=config.IS_INNER_SERVER
	dProtocol={'service':(	centerService.service.cService,
							collect.service4main.cService,
						),
				'stub':(	backEnd_center_pb2.center2backEnd_Stub,
							center_collect_pb2.center2backEnd_Stub,
						)
				}
	ep=cEndPointWithSocket(bDebugMode,dProtocol)
	iEndPointId=nextEndPointId()
	ep.setEndPointId(iEndPointId)
	ep.setIP(sIP).setPort(iPort).setSocket(oSocket)
	gBackEndKeeper.addObj(ep,iEndPointId)
	ep.start()

	ep.join()

def initServer():
	iListenPort=config.CENTER_PORT
	oServer=gevent.server.StreamServer(('0.0.0.0',iListenPort),u.cFunctor(afterAccept,iListenPort))
	print ('starting center server on port {}'.format(iListenPort))
	return oServer

import keeper
import u

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'centerService' in SYS_ARGV:
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
import config

import c
import p
import misc
import log
import timeU
import timer
import codec
