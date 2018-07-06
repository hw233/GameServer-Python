# -*- coding: utf-8 -*-
import endPoint
import terminal_chat_pb2

class cService(terminal_chat_pb2.chat2terminal):
	
	@endPoint.result
	def rpcBanChannelRes(self, ep, ctrl, reqMsg):return rpcBanChannelRes(ep, ctrl, reqMsg)
	
	
def rpcBanChannelRes(ep, ctrl, reqMsg):
	print "rpcBanChannelRes", str(reqMsg).replace("\n", ",")