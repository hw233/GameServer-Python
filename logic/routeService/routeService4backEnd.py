#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_route_pb2
import endPoint
import misc

class cService(backEnd_route_pb2.backEnd2route):
	@endPoint.result
	def rpcBackEndReport(self,ep,who,reqMsg):return rpcBackEndReport(self,ep,who,reqMsg)

def rpcBackEndReport(self,ep,ctrlr,reqMsg):#
	iBackEndType=reqMsg.iValue
	if iBackEndType not in (1,2,4,8,16,32,64):
		raise Exception,'backEnd的类型只能是1,2,4,8,16,32,64'
	sBackEndName=backEnd.gdServiceName[iBackEndType]
	
	sText='{}来报到,ip:{},port:{}'.format(sBackEndName,ep.ip(),ep.port())
	print sText  #'后端"{}"向路由报到'.format(sBackEndName)

	ep.setBackEndType(iBackEndType)
	routeServer4backEnd.gBackEndProxy.addObj(ep,iBackEndType)
	log.log('rpc',sText)
	
	# ev=routeService.gdBackEndReport2routeEvent.get(iBackEndType)#后端报到事件
	# if ev:
	# 	ev.set()

	for (iHasReportBackEnd,),oBackEnd in routeServer4backEnd.gBackEndProxy.getAll().items(): #dictionary changed size during iteration
		if iHasReportBackEnd==iBackEndType:
			continue
		#全部后端互相通知一下	
		ep.rpcOtherBackEndLink2route(iHasReportBackEnd)
		oBackEnd.rpcOtherBackEndLink2route(iBackEndType)#通知其他backEnd,有人来报到
	return True

# def rpcShutdownGameClient(self,ep,ctrlr,reqMsg):#逻辑服务命令路由服务关闭某一个客户端连接
# 	iConnId=reqMsg.iValue
# 	oClient=server4gameClient.gConnKeeper.getObj(iConnId)
# 	if oClient:
# 		sText='后端通知路由,叫路由shutdown一个客户端连接.connId={},ip={},port={}'.format(iConnId,oClient.ip(),oClient.port())
# 		print sText
# 		log.log('rpc',sText)
# 		oClient.shutdown()

# 	#不在这里通知到其他后端,由shutdown触发 send和recv协程结束时再发rpcGameClientDisConnected
# 	# for (iBackEndType,),oBackEnd in routeServer4backEnd.gBackEndProxy.getAll().iteritems():
# 	# 	if iBackEndType==ctrlr.iBackEndType:#跳过主动发起的后端	
# 	# 		continue 
# 	# 	oBackEnd.rpcGameClientDisConnected(iConnId)#通知其他backEnd,有客户端连接断了
# 	return True
	
import c
import u
import log


import timeU
import mysqlCnt
import account
import role
import mainService
import gateService
import routeServer4backEnd
import backEnd
import init