# -*- coding: utf-8 -*-
import endPoint
import scene_pb2

class cService(scene_pb2.main2terminal):
	
	@endPoint.result
	def rpcSwitchScene(self, ep, ctrl, reqMsg):return rpcSwitchScene(ep, ctrl, reqMsg)
	
def rpcSwitchScene(ep, ctrl, reqMsg):
# 	print "rpcSwitchScene", "roleId:%d" % ep.roleId, str(reqMsg).replace("\n", ",")
	roleId = ep.roleId
	who = robot.getClientRole(roleId)
	if not who:
		return
	
	data = {
		"sceneId": reqMsg.iSceneId,
		"x": reqMsg.x,
		"y": reqMsg.y,
	}
	who.updateAttr(data)
	
	if hasattr(who, "logining"): # 登录完毕，开始AI
		del who.logining
		robot.ai.startAI(who)
	

def rpcMove(who):
# 	print "rpcMove", scene.validPos(who.sceneId, who.x, who.y), "roleId:%d,sceneId:%d,x:%d,y:%d" % (who.id, who.sceneId, who.x, who.y)
	msg = {
		"iEttId": who.id,
		"sceneId": who.sceneId,
		"x": who.x,
		"y": who.y,
	}
	who.endPoint.rpcRoleMove(**msg)
	
def rpcWorldTransfer(who, sceneId):
	'''传送指定地图，默认坐标
	'''
	who.endPoint.rpcWorldTransfer(sceneId)
	
def rpcRobotTransfer(who, sceneId, x, y):
	'''传送指定地图，指定坐标
	'''
	who.sceneId = sceneId
	who.x = x
	who.y = y
	who.endPoint.rpcRobotTransfer(sceneId, x, y)

import robot
import scene
	