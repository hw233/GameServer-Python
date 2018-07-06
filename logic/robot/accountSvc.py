# -*- coding: utf-8 -*-
import endPoint
import account_pb2

class cService(account_pb2.main2terminal):pass

# 	@endPoint.result
# 	def rpcRoleList(self, ep, ctrl, reqMsg):return rpcRoleList(ep, ctrl, reqMsg)
	
# def rpcRoleList(ep, ctrl, reqMsg):
# 	print "rpcRoleList", str(reqMsg).replace("\n", ",")
# 	roleList = reqMsg.roles
# 	if len(roleList):
# 		roleId = roleList[0].iRoleId,
# 		rpcRoleLogin(ep, roleId)
# 	else:
# 		rpcCreateRole(ep)
	
	
def rpcRobotLogin(ep, accountName):
	'''机器人登录
	'''   
	ep.rpcRobotLogin(accountName)
	
# def rpcCreateRole(ep):
# 	'''创建角色
# 	'''
# 	accountName = ep.accountName
# 	data = robotData.getRobotData(accountName)
# 	school = data["门派"]
# 	shapeList = data["造型"]
# 	shape = shapeList[rand(len(shapeList))]
# 	ep.rpcCreateRole(school, shape)
# 	
# def rpcRoleLogin(ep, roleId):
# 	'''角色登录
# 	'''
# 	ep.rpcRoleLogin(roleId)
	
	
from common import *
import gevent
import client
import config
import robot
import robot.object
import robot.service
import robotData
