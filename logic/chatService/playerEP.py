# -*- coding: utf-8 -*-
import endPointWithoutSocket

class cPlayerEndPoint(endPointWithoutSocket.cEndPointWithoutSocket):
	
	def __init__(self, *tArgs, **dArgs):  # override
		endPointWithoutSocket.cEndPointWithoutSocket.__init__(self, *tArgs, **dArgs)
		self.iRoleId = 0

	def _getEP2send(self):  # override
		return client4gate.getGateEp4cs()
	
	def _getControllerForDealRequest(self, sMethodName, iReqId):  # override 获取ctrl,在处理对端的请求时
		if self.iRoleId == 0:
			return "该连接对应的角色还没有注册到此服"

		senderObj = chatService.getSender(self.iRoleId)
		if senderObj:
			return senderObj
		return "找不到角色发送者"

	def setAssociativeRole(self, iRoleId):  # 为endPoint设置关联的角色id
		self.resetAssociativeRole()  # 先重置一下再说
		self.iRoleId = iRoleId
		chatService.gRoleIdMapEndPoint.addObj(self, self.iRoleId)

	def resetAssociativeRole(self):  # 重置,不再关联角色id
		if 0 == self.iRoleId:
			return
		chatService.gRoleIdMapEndPoint.removeProxy(self.iRoleId)
		
	def _nextRequestId(self): #override
		self.iLastRequestId = u.guIdWithPostfix(backEnd_pb2.CHAT_SERVICE,self.iLastRequestId,True)
		return self.iLastRequestId

import client4gate
import chatService
import backEnd_pb2
