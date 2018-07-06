#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import endPointWithSocket
import instruction

class combineService(
	#这里面的class实现每一个成员方法时,都调用另一个全局方法,
	#因为成员方法都加了装饰器,加了装饰器形成闭包后会热更新失败,
	#全局方法因为没有装饰器,所以可以热更新
	instruction.cService,
	):
	pass

def afterAccept(sock,tAddress):
	sIP,iPort=tAddress
	#这里可以控制总连接数sock.shutdown()
	print 'instruction server:new connection from ip:{} port:{}'.format(sIP,iPort)
	log.log('instructionServerConnection','ip:{} port:{}'.format(sIP,iPort))#记log

	bDebugMode=config.IS_INNER_SERVER
	ep=cEndPointWithSocket(bDebugMode,(combineService,terminal_main_pb2.main2terminal_Stub))
	ep.setEndPointId(nextEndPointId())
	ep.setIP(sIP).setPort(iPort).setSocket(sock)
	ep.start()
	gEndPointKeeper.addObj(ep,ep.epId())
	ep.join()
	
def initServer():
	iPort=config.INSTRUCTION_PORT
	oServer=gevent.server.StreamServer(('0.0.0.0',iPort),afterAccept)
	print ('starting instruction server on port {}'.format(iPort))
	return oServer

class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,*tArgs,**dArgs):#override
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)
		self.iRoleId=0 #算是interface ,instruction模块要访问这个属性

	def group(self):#所属gm权限组(本服务的端口只开放在防火墙内的局域网,但凡连上此端口的都给最大权限)
		return instruction.ADMIN

	#根据不同方法名取得不同的对象,若是返回假值,表示没有通过授权
	#这里return的对象必须是controller子类的实例
	def _getControllerForDealRequest(self,sMethodName,iReqId):#override 获取ctrl,在处理对端的请求时		
		return self

	def _onDisConnected(self):#override
		gEndPointKeeper.removeObj(self.epId())		
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)

def nextEndPointId():
	global giEndPointId
	if 'giEndPointId' not in globals():
		giEndPointId=0
	giEndPointId+=1
	return giEndPointId

import keeper

if 'gEndPointKeeper' not in globals():
	gEndPointKeeper=keeper.cKeeper()#channel id 映射 channel

import gevent.server
import u
import c
import misc
import log
import terminal_main_pb2
import timeU
import config