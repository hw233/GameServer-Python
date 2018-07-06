# -*- coding: utf-8 -*-
import endPoint
import terminal_main_pb2

class cService(terminal_main_pb2.main2terminal):

	@endPoint.result
	def rpcAvatarAttrInit(self, ep, ctrl, reqMsg):return rpcAvatarAttrInit(ep, ctrl, reqMsg)
	
def rpcAvatarAttrInit(ep, ctrl, reqMsg):
	roleData = {}
	for obj, val in reqMsg.ListFields():
		roleData[obj.name] = val
	
	accountName = ep.accountName
	roleId = roleData["roleId"]
	who = robot.createClientRole(accountName, roleId)
	who.updateAttr(roleData)
	robot.gClientRoleList[roleId] = who
	ep.roleId = roleId
	who.logining = True # 正在登录中
	writeLog("login", "acount:%s roleId:%s login success" % (accountName, roleId))

from common import *
import robot
import robot.ai