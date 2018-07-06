#-*-coding:utf-8-*-

import center_collect_pb2
import endPoint
import misc


#中心服-->主服
class cService(center_collect_pb2.center2backEnd):
	@endPoint.result
	def rpcCenterCollectTest(self,ep,ctrlr,reqMsg): return rpcCenterCollectTest(ctrlr,reqMsg)

	@endPoint.result
	def rpcC2BCollectAddEvent(self,ep,ctrlr,reqMsg): return rpcC2BCollectAddEvent(ctrlr,reqMsg)

	@endPoint.result
	def rpcC2BCollectDelEvent(self,ep,ctrlr,reqMsg): return rpcC2BCollectDelEvent(ctrlr,reqMsg)

def rpcCenterCollectTest(ctrlr,reqMsg):
	pass
	# print "=====rpcCenterCollectTest:中心服-->主服协议",ctrlr,reqMsg

def rpcC2BCollectAddEvent(ctrlr,reqMsg):
	iRoleId = reqMsg.iRoleId
	who = getRole(iRoleId)
	if not who:
		return
	who.send(reqMsg.sSerialized)

def rpcC2BCollectDelEvent(ctrlr,reqMsg):
	iRoleId = reqMsg.iRoleId
	who = getRole(iRoleId)
	if not who:
		return
	who.send(reqMsg.sSerialized)




from common import *
import log
import c
import u
import misc
import role
import backEnd
import backEnd_pb2
import client4center
import collect
import collect_pb2
import endPoint


