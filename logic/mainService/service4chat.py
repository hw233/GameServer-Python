# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import main_chat_pb2
import endPoint

class cService(main_chat_pb2.chat2main):
	@endPoint.result
	def rpcHelloMain_iAmChat(self, ep, ctrlr, reqMsg):return rpcHelloMain_iAmChat(self, ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcCostHuoli(self, ep, ctrlr, reqMsg):return rpcCostHuoli(self, ep, ctrlr, reqMsg)

def rpcCostHuoli(self, ep, ctrlr, reqMsg):
	'''扣除活力
	'''
	roleId = reqMsg.roleId
	costVal = reqMsg.costVal
	who = getRole(roleId)
	if not who:
		return False
	if who.huoli < costVal:
		return False
	who.addHuoli(-costVal, "发言")
	return True

def rpcHelloMain_iAmChat(self, ep, ctrlr, reqMsg):
	print "rpcHelloMain_iAmChat 被call"
	return True

from common import *
