#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import client
import endPointWithSocket
#import meshService_pb2
import account_pb2
#mesh客户端


class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,iZoneNo,*tArgs,**dArgs):		
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)
		self.iZoneNo=iZoneNo

	def zoneNo(self):
		return self.iZoneNo

	def _onDisConnected(self):
		print 'mesh客户端zoneNo={}断线了.'.format(self.iZoneNo)
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		oClient=gMeshClientKeeper.getObj(self.iZoneNo)
		if not oClient:
			return
		oClient.connect(0)#断线了,要尝试重连.

def afterConnect(sock,tAddress,iZoneNo):
	sIP,iPort=tAddress
	print 'mesh client(zoneNo={}):connect success to ip:{} port:{}'.format(iZoneNo,*tAddress)
	oClient=gMeshClientKeeper.getObj(iZoneNo)
	if not oClient:
		return
	bDebugMode=config.IS_INNER_SERVER
	ep=cEndPointWithSocket(iZoneNo,bDebugMode,(None,meshService_pb2.serverService_Stub))
	ep.setIP(sIP).setPort(iPort).setSocket(sock)
	ep.start()
	return ep
	
def start(iZoneNo,sIp='127.0.0.1'):	
	iPort=config.MESH_PORT
	oClient=client.cStreamClient((sIp,iPort),u.cFunctor(afterConnect,iZoneNo))
	gMeshClientKeeper.addObj(oClient,iZoneNo)
	
	print ('mesh client(zoneNo={}):starting try to connect to ip:{} port:{}'.format(iZoneNo,sIp,iPort))
	oClient.connect(0)

import keeper

if 'gMeshClientKeeper' not in globals():
	gMeshClientKeeper=keeper.cKeeper()

import socket
import traceback
import gevent
import gevent.socket
import gevent.queue


import misc
import u
import log
import config