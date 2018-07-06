#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#拼装各种服务
import gevent.pool
import gevent.greenlet
import endPointWithSocket
#import meshService_pb2
import meshServerService

class combineService(
	#这里面的class实现每一个成员方法时,都调用另一个全局方法,
	#因为成员方法都加了装饰器,加了装饰器形成闭包后会热更新失败,
	#全局方法因为没有装饰器,所以可以热更新
	meshServerService.cService,
	):	
	def __init__(self,ep):
		self.ep=ep

def afterAccept(sock,tAddress):
	sIP,iPort=tAddress
	#这里可以控制总连接数sock.shutdown()
	print 'mesh server:new connection from ip:{} port:{}'.format(*tAddress)
	#记log
	bDebugMode=config.IS_INNER_SERVER
	ep=cEndPointWithSocket(bDebugMode,(combineService,None))
	ep.setEndPointId(nextEndPointId())
	ep.setIP(sIP).setPort(iPort).setSocket(sock)
	ep.start()
	gEndPointKeeper.addObj(ep,ep.epId())
	
def init():
	iPort=config.MESH_PORT
	oServer=gevent.server.StreamServer(('0.0.0.0',iPort),afterAccept)
	print ('starting mesh server on port {}'.format(iPort))
	return oServer

class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,*tArgs,**dArgs):#override
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)
		self.iZoneNo=0
		self.bGranted=False #是否已经通过账号密码之类的验证
		
	def setGranted(self):
		self.bGranted=True
	
	def setZoneNo(self,iZoneNo):#设置区号并关联channel
		self.iZoneNo=iZoneNo
		gdZoneNoMapEndPoint[iZoneNo]=gEndPointKeeper.getObj(self.epId())
	
	def zoneNo(self):
		return self.iZoneNo	

	def copyFrom(self,ep):#override
		endPointWithSocket.cEndPointWithSocket.copy(self,ep)
		self.bGranted=ep.bGranted
		self.iZoneNo=ep.iZoneNo

	#根据不同方法名取得不同的对象,若是返回假值,表示没有通过授权
	#这里return的对象必须是controller子类的实例
	def _getControllerForDealRequest(self,sMethodName,iReqId):#override 获取ctrl,在处理对端的请求时
		return self
	
	def _workerJobProc(self,fRecvStamp,req):#override,在异常信息中加上区号
		try:
			endPointWithSocket.cEndPointWithSocket._workerJobProc(self,fRecvStamp,req)
		except Exception:
			if self.iZoneNo!=0:
				u.reRaise('区号={}.'.format(self.iZoneNo))
			else:
				raise

	def _onDisConnected(self):#override
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		gEndPointKeeper.removeObj(self.epId())
		gdZoneNoMapEndPoint.pop(self.iZoneNo,None)

def nextEndPointId():
	global giEndPointId
	if 'giEndPointId' not in globals():
		giEndPointId=0
	giEndPointId+=1
	return giEndPointId

def getEndPointByZoneNo(iZoneNo):
	return gdZoneNoMapEndPoint.get(iZoneNo)

if 'gdZoneNoMapEndPoint' not in globals():
	gdZoneNoMapEndPoint={}#区号映射channel,value是proxy

import keeper

if 'gEndPointKeeper' not in globals():
	gEndPointKeeper=keeper.cKeeper()

import traceback
import socket
import gevent
import gevent.server
import u
import c
import misc
import log
import terminal_main_pb2
import account

import role
import config