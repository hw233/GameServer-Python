#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_route_pb2
import endPoint
import misc
import config

class cService(backEnd_route_pb2.route2backEnd):
	@endPoint.result
	def rpcOtherBackEndLink2route(self,ep,ctrlr,reqMsg):return rpcOtherBackEndLink2route(self,ep,ctrlr,reqMsg)

def rpcOtherBackEndLink2route(self,ep,ctrlr,reqMsg):#有其他backEnd连接到路由
	iReportBackEnd=reqMsg.iValue
	sBackEndName=backEnd.gdServiceName[iReportBackEnd]
	backEnd.backEndEvent.channelBuilt(iReportBackEnd,1)

import c
import timeU
import u
import log
import gateService
import backEnd
import backEnd.backEndEvent