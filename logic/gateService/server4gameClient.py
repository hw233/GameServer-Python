#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_pb2
#客户端连接
class cGameClientConnection(object):
	def __init__(self,iConnId,oSocket,sIP,iPort):
		self.iConnId=iConnId
		self.sSerializedConnId=p.cPack().packInt(gateService.CONN_ID_SIZE,self.iConnId).getBuffer()
		self.oSocket=oSocket
		self.sIP=sIP
		self.iPort=iPort
		self.sendQueue=gevent.queue.Queue()
		#这里不需要recv queue ,收到数据时直接塞到主逻辑服或场景服的发送队列
		self.recvQueue=gevent.queue.Queue(1) #增加recv queue,避免客户端恶意频繁发包
		self.sendJob=self.recvJob=self.send2BackEndJob=None
		self.bHasStopIteration=False #sendQueue已经放入了StopIteration,即是服务器主动关闭
		self.hangEvent=gevent.event.Event()
		self.wr=gTimingWheel.makeWrObj(self.__deleter)#makeWrObj里面会防止循环引用
		self.iCreateStamp=timeU.getStamp()#创建时间

	def __deleter(self,wr):
		try:
			if config.IS_INNER_SERVER:
				return

			iLife=timeU.getStamp()-self.iCreateStamp

			sText='久未操作系统自动踢除,IP={},port={},connId,存活时间={}'.format(self.sIP,self.iPort,iLife)
			log.log('kick',sText)
			self.shutdown()
			# sText='系统自动踢除,roleId={},userSource={},account={},endPointId={},存活时间={}'.format(self.iRoleId,self.sUserSource,self.sAccount,self.epId(),iLife)
			# log.log('kick',sText)
		except Exception:
			misc.logException()		

	def ip(self):
		return self.sIP

	def port(self):
		return self.iPort
		
	def send(self,iFrom,sPacket):#logic客户端会塞StopIteration进来
		if self.bHasStopIteration or not self.sendJob:#关闭中,或sendjob已dead
			return
		#todo 队列满了,证明客户端收不过来,或许应该砍掉这个连接.
		self.sendQueue.put(sPacket)

	def shutdown(self,fSecond=2):#logic客户端会塞StopIteration进来
		if self.bHasStopIteration or not self.sendJob:#关闭中,或sendjob已dead
			return
		self.bHasStopIteration=True	
		self.sendQueue.put(StopIteration)
		try:
			self.recvJob.get(True,fSecond)#n秒内要收到客户端的fin,因为客户端可能收fin后但是就不愿意shutdown(恶意的客户端)
		except gevent.timeout.Timeout:
			self.recvJob.kill()

	def start(self):
		self.recvJob=gevent.spawn(u.cFunctor(self.__recvLoop))
		self.sendJob=gevent.spawn(u.cFunctor(self.__sendLoop))
		self.send2BackEndJob=gevent.spawn(u.cFunctor(self.__send2BackEndLoop))

		self.recvJob.link(u.cFunctor(self.__afterRecvJobExit))
		self.sendJob.link(u.cFunctor(self.__afterSendJobExit))
		self.send2BackEndJob.link(u.cFunctor(self.__afterSend2BackEndJobExit))

		self.hangEvent.wait()

	def __where2send(self,sBuffer):#返回(request,methodName)或(非request,id)
		packet=universal.public_pb2.packet()
		packet.ParseFromString(sBuffer)
		if packet.iType==universal.public_pb2.TYPE_REQUEST:
			req=universal.public_pb2.request()
			req.ParseFromString(packet.sSerialized)
			return _getPacketTarget(req.sMethodName)
		else:
			response=universal.public_pb2.response()
			response.ParseFromString(packet.sSerialized)
			#直接弹出来了,即是此函数同一个request id只能被调用一次
			# print "which backEnd:",u.getNoByguId(response.iResponseId)
			return u.getNoByguId(response.iResponseId)
			
	def __recvLoop(self):
		decoder=codec.cDecoder(1*1024*1024) #最大能接收的逻辑包大小,1兆
		oBuffer=buf.cBuffer()
		while True:
			mv=oBuffer.peekWrite()
			try:#非正常关闭是常有的事,不抛异常这么难看				
				iSize=self.oSocket.recv_into(mv)#
			except socket.error:
				return
			if 0==iSize:#收到了Fin分节
				return #表示收到fin分节,正常友好地关闭
			oBuffer.hasWritten(iSize)
				
			for sPacket in decoder.decode(oBuffer):
				self.recvQueue.put(sPacket)
				obj=self.wr()
				if obj:
					gTimingWheel.addObj(obj)
					obj=None  #因为不会跳出while循环，obj局部变量会一直在，所以要设为空。

	def __send2BackEndLoop(self):
		try:
			for sPacket in self.recvQueue:
				iTarget=self.__where2send(sPacket)
				#根据网络包类型分发到不同的后端服务
				backEndEP=gateServer4backEnd.gBackEndProxy.getProxy(iTarget)
				if backEndEP:
					backEndEP.send(sPacket,self.sSerializedConnId)
				else:
					raise Exception,'网关收到游戏客户端的包,但网关与类型为{}的后端服务的连接不存在,无法转发.'.format(iTarget)

		except socket.error:
			return

	def __sendLoop(self):
		encoder=codec.cEncoder()
		try:#非正常关闭是常有的事,不抛异常这么难看
			for sPacket in self.sendQueue:
				self.oSocket.sendall(encoder.encode(sPacket))
		except socket.error:
			return
		self.oSocket.shutdown(1) #关闭写

	def __afterRecvJobExit(self,recvJob):
		if self.sendJob:
			self.sendJob.kill()
		if self.send2BackEndJob:
			self.send2BackEndJob.kill()
				
		#通知全部backEnd,有客户端连接断了
		for (iBackEndType,),oBackEnd in gateServer4backEnd.gBackEndProxy.getAll().iteritems():
			oBackEnd.rpcGameClientDisConnected(self.iConnId)#全关闭

		self.oSocket.close()#真正地全关闭	
		self.__onDisConnected()

	def __afterSendJobExit(self,sendJob):
		if self.recvJob:
			self.recvJob.kill()
		if self.send2BackEndJob:
			self.send2BackEndJob.kill()

	def __afterSend2BackEndJobExit(self,send2BackEndJob):
		if self.recvJob:
			self.recvJob.kill()
		if self.sendJob:
			self.sendJob.kill()

	def __onDisConnected(self):
		self.hangEvent.clear()
		print '一个游戏客户端连接断开了'
		gConnKeeper.removeObj(self.iConnId)

def afterAccept(oSocket,tAddress,iGateServiceId):
	sIP,iPort=tAddress
	#这里可以控制总连接数sock.shutdown()
	print 'gate stream service for game client:new connection from ip:{} port:{}'.format(sIP,iPort)	
	log.log('connection4gameClient','ip:{} port:{}'.format(sIP,iPort))#记log

	gdeqRecentConnection.append('{} {}:{}'.format(timeU.stamp2str(),sIP,iPort))
	while len(gdeqRecentConnection)>20:#40
		gdeqRecentConnection.popleft()

	iConnId=genConnId(iGateServiceId)#后端也用此id标识一个连接
	#通知全部后端服务新建立了一个连接
	for iBackEndType,oBackEnd in gateServer4backEnd.gBackEndProxy.getAll().items():
		bFail,uMsg=oBackEnd.rpcGameClientConnect(iGateServiceId,iConnId,sIP,iPort)
		if bFail:
			continue
	#print 'rpcGameClientConnect=',uMsg.iValue
	oConnection=cGameClientConnection(iConnId,oSocket,sIP,iPort)
	gConnKeeper.addObj(oConnection,iConnId)
	oConnection.start()

def initServer(iGateServiceId=1):
	global giGateServiceId
	giGateServiceId = iGateServiceId
	iPort=config.GATE_PORT_FOR_GAME_CLIENT
	oServer=gevent.server.StreamServer(('0.0.0.0',iPort),u.cFunctor(afterAccept,iGateServiceId))
	print ('starting gate server for game client on port {}'.format(iPort))
	return oServer

def genConnId(iGateServiceId=1):#生成连接id,以网关服务id作后缀,多个网关生成各自不重复的连接id,能同时工作
	global giConnId
	if giConnId==0:
		giConnId=u.guIdWithPostfix(iGateServiceId,0,False)
	else:
		giConnId=u.guIdWithPostfix(iGateServiceId,giConnId,True)
	return giConnId


import gateService

def _getPacketTarget(sMethodName):#根据rpc名字决定发往哪个后端
	for iBackEnd,lServie in gdService.iteritems():
		for oService in lServie:
			try:#FindMethodByName当找不到时,C++版本会抛异常,python版本会返回None,行为不一致
				methodDescriptor=oService.GetDescriptor().FindMethodByName(sMethodName)
				if methodDescriptor:
					return iBackEnd
			except:
				pass

	return backEnd_pb2.MAIN_SERVICE #找不到就往主逻辑服务发

import client4gate.service4gate

gdService={
	backEnd_pb2.SCENE_SERVICE:[],
	backEnd_pb2.CHAT_SERVICE:[],	
	backEnd_pb2.FIGHT_SERVICE:[],
	#backEnd_pb2.MAIN_SERVICE:[],
}
for serviceCls in client4gate.service4gate.gdSceneService.get('service',()):
	gdService[backEnd_pb2.SCENE_SERVICE].append(serviceCls())

for serviceCls in client4gate.service4gate.gdChatService.get('service',()):
	gdService[backEnd_pb2.CHAT_SERVICE].append(serviceCls())

for serviceCls in client4gate.service4gate.gdFightService.get('service',()):
	gdService[backEnd_pb2.FIGHT_SERVICE].append(serviceCls())	

import keeper
import collections
import gateService.timingWheel

if 'gbOnce' not in globals():
	gbOnce=True

	if 'gateService' in SYS_ARGV:
		giConnId=0
		gConnKeeper=keeper.cKeeper()#连接id 映射 连接对象

		gdeqRecentConnection=collections.deque()#双端队列,记录最近的连接信息

		gTimingWheel=gateService.timingWheel.cTimingWheel(6,10)#刻度数,间隔秒数 6*10=60秒
	
import socket

import gevent
import gevent.server
import gevent.queue
import gevent.core
import gevent.event
import universal.public_pb2

import u
import c
import p
import misc
import log
import timeU
import timer
import codec
import gateServer4backEnd
import config
import buf


#==================================
#单独启动场景服时，恢复网关到场景服的客户端连接
if 'giGateServiceId' not in globals():
	giGateServiceId = 0	#用来恢复

def recoverySSGameClientConnect(oSceneBackEnd):
	if not giGateServiceId:
		return
	
	for uConnId,oConnection in gConnKeeper.getIterItems():
		iConnId = uConnId[0]
		bFail,uMsg=oSceneBackEnd.rpcGameClientConnect(giGateServiceId,iConnId,oConnection.sIP,oConnection.iPort)
		if bFail:
			continue

	#通知主服恢复
	oMainBackEnd = gateServer4backEnd.gBackEndProxy.getProxy(1)
	if not oMainBackEnd:
		return

	oMainBackEnd.rpcRecoverySceneService()

