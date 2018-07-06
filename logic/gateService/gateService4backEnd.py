#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_gate_pb2
import endPoint
import misc

class cService(backEnd_gate_pb2.backEnd2gate):
	@endPoint.result
	def rpcShutdownGameClient(self,ep,who,reqMsg):return rpcShutdownGameClient(self,ep,who,reqMsg)

	@endPoint.result
	def rpcBackEndReport(self,ep,who,reqMsg):return rpcBackEndReport(self,ep,who,reqMsg)

	@endPoint.result
	def rpcHelloGate(self,ep,who,reqMsg):return rpcHelloGate(self,ep,who,reqMsg)

def rpcHelloGate(self,ep,ctrlr,reqMsg):#
	print 'rpcHelloGate called'
	return True


def rpcBackEndReport(self,ep,ctrlr,reqMsg):#
	iBackEndType=reqMsg.iValue
	if iBackEndType not in (1,2,4,8,16,32,64):
		raise Exception,'backEnd的类型只能是1,2,4,8,16,32,64'
	sBackEndName=backEnd.gdServiceName[iBackEndType]
	sText='{}来报到,ip:{},port:{}'.format(sBackEndName,ep.ip(),ep.port())
	print sText
	ep.setBackEndType(iBackEndType)
	gateServer4backEnd.gBackEndProxy.addObj(ep,iBackEndType)
	log.log('rpc',sText)

	
	ev=gateService.gdBackEndReport2gateEvent.get(iBackEndType)#后端报到事件,init.py里面还等着开端口给客户端连接
	if ev:
		ev.set()

	for (iHasReportBackEnd,),oBackEnd in gateServer4backEnd.gBackEndProxy.getAll().iteritems():
		if iHasReportBackEnd==iBackEndType:
			continue
		#全部后端互相通知一下
		ep.rpcOtherBackEndLink2gate(iHasReportBackEnd)
		oBackEnd.rpcOtherBackEndLink2gate(iBackEndType)#通知其他backEnd,有人来报到
	
	if iBackEndType == 2:#场景服报到时恢复已有客户端连接
		server4gameClient.recoverySSGameClientConnect(ep)
	return True

def rpcShutdownGameClient(self,ep,ctrlr,reqMsg):#逻辑服务命令网关服务关闭某一个客户端连接
	iConnId=reqMsg.iValue
	oClient=server4gameClient.gConnKeeper.getObj(iConnId)
	if oClient:
		sText='后端通知网关,叫网关shutdown一个客户端连接.connId={},ip={},port={}'.format(iConnId,oClient.ip(),oClient.port())
		print sText
		log.log('rpc',sText)
		oClient.shutdown()

	#不在这里通知到其他后端,由shutdown触发 send和recv协程结束时再发rpcGameClientDisConnected
	# for (iBackEndType,),oBackEnd in gateServer4backEnd.gBackEndProxy.getAll().iteritems():
	# 	if iBackEndType==ctrlr.iBackEndType:#跳过主动发起的后端	
	# 		continue 
	# 	oBackEnd.rpcGameClientDisConnected(iConnId)#通知其他backEnd,有客户端连接断了
	return True
	
import c
import u
import log


import timeU
import mysqlCnt
import account
import role
import mainService
import gateService
import gateServer4backEnd
import server4gameClient
import init
import backEnd