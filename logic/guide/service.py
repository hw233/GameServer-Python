# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import endPoint
import guide_pb2


class cService(guide_pb2.terminal2main):

	@endPoint.result
	def rpcGuideAddRecord(self, ep, who, reqMsg): return rpcGuideAddRecord(who, reqMsg)

	@endPoint.result
	def rpcGuideEndRecord(self, ep, who, reqMsg): return rpcGuideEndRecord(who, reqMsg)

	@endPoint.result
	def rpcGuideNewRecord(self, ep, who, reqMsg): return rpcGuideNewRecord(who, reqMsg)
	

def rpcGuideAddRecord(who, reqMsg):
	'''引导做完记录
	'''
	guideRecord = who.fetch("guide", {})
	guideRecord["guideNo"] = reqMsg.iValue
	who.set("guide", guideRecord)

def rpcGuideEndRecord(who, reqMsg):
	'''是否结束
	'''
	guideRecord = who.fetch("guide", {})
	guideRecord["guideEnd"] = reqMsg.iValue
	who.set("guide", guideRecord)

def rpcGuideNewRecord(who, reqMsg):
	'''是否新手
	'''
	guideRecord = who.fetch("guide", {})
	guideRecord["isNew"] = reqMsg.iValue
	who.set("guide", guideRecord)

def sendGuideRecord(who):
	'''发送引导记录
	'''
	guideRecord = who.fetch("guide", {})
	msg = {}
	msg["iGuideNo"] = guideRecord.get("guideNo", 0)
	msg["iIsEnd"] = guideRecord.get("guideEnd", 0)
	msg["iIsNew"] = guideRecord.get("isNew", 1)
	who.endPoint.rpcGuideRecord(**msg)
	
def changeGuideNo(who, guideNo):
	'''改变新手引导编号
	'''
	guideRecord = who.fetch("guide", {})
	guideRecord["guideNo"] = guideNo
	who.set("guide", guideRecord)
	who.endPoint.rpcGuideChangeGuideNo(guideNo)

from common import *
import message
