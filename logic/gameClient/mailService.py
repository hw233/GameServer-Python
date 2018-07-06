# -*- coding: utf-8 -*-
import endPoint
import mail_pb2

class cService(mail_pb2.main2terminal):
	
	@endPoint.result
	def rpcMailListAll(self, ep, ctrl, reqMsg):return rpcMailListAll(ep, ctrl, reqMsg)
	
	@endPoint.result
	def rpcMailAdd(self, ep, ctrl, reqMsg):return rpcMailAdd(ep, ctrl, reqMsg)
	
	@endPoint.result
	def rpcMailChange(self, ep, ctrl, reqMsg):return rpcMailChange(ep, ctrl, reqMsg)
	
def rpcMailListAll(ep, ctrl, reqMsg):
	print "rpcMailListAll", str(reqMsg).replace("\n", ",")
	
def rpcMailAdd(ep, ctrl, reqMsg):
	print "rpcMailAdd", str(reqMsg).replace("\n", ",")
	
def rpcMailChange(ep, ctrl, reqMsg):
	print "\nrpcMailChange", str(reqMsg).replace("\n", ",")
	print "\n", reqMsg.HasField("title")
	print "\n", reqMsg.HasField("propsList")
	for obj, v in reqMsg.ListFields():
		print obj.name, v