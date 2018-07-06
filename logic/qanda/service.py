# -*- coding: utf-8 -*-
'''问答服务
'''
import endPoint
import qanda_pb2

class cService(qanda_pb2.terminal2main):

	@endPoint.result
	def rpcInputBoxResponse(self, ep, who, reqMsg): return rpcInputBoxResponse(who, reqMsg)
	
	@endPoint.result
	def rpcWalkToPosResponse(self, ep, who, reqMsg): return rpcWalkToPosResponse(who, reqMsg)
	
	@endPoint.result
	def rpcSelectBoxResponse(self, ep, who, reqMsg): return rpcSelectBoxResponse(who, reqMsg)
	
	@endPoint.result
	def rpcConfirmBoxResponse(self, ep, who, reqMsg): return rpcConfirmBoxResponse(who, reqMsg)

	@endPoint.result
	def rpcTeamConfirmBoxResponse(self, ep, who, reqMsg): return rpcTeamConfirmBoxResponse(who, reqMsg)
	
	@endPoint.result
	def rpcPopPropsResponse(self, ep, who, reqMsg): return rpcPopPropsResponse(who, reqMsg)
	
	@endPoint.result
	def rpcProgressBarResponse(self, ep, who, reqMsg): return rpcProgressBarResponse(who, reqMsg)

	

#===============================================================================
# 输入框	
#===============================================================================
def rpcInputBoxResponse(who, reqMsg):
	'''输入框回应
	'''
	handlerId = reqMsg.validId
	content = reqMsg.responseVal
	if not content:
		return
	handler = qanda.popResponseHandler(who, handlerId)
	if handler:
		handler.handle(who, content)
		
def rpcInputBoxRequest(who, responseFunc, title, content, limitType=0, limitLength=0):
	'''弹出输入框
	'''
	responseCheckFunc = functor(checkInputBoxResponse, limitType, limitLength)
	handlerId = qanda.setupResponseHandler(who, responseFunc, responseCheckFunc)
	msg = {
		"validId": handlerId,
		"title": title,
		"content": content,
		"limitType": limitType,
		"limitLength": limitLength,
	}
	who.endPoint.rpcInputBoxRequest(**msg)
	
def checkInputBoxResponse(who, content, limitType, limitLength):
	'''检查输入回应
	'''
	if limitType == TYPE_LIMIT_INT:
		if not re.match("^[-+]?\d+$", content):
			return 0
	if limitLength and calLen(content) > limitLength:
		return 0
	return 1


#===============================================================================
# 寻路
#===============================================================================
def rpcWalkToPosResponse(who, reqMsg):
	'''寻路回应
	'''
	handlerId = reqMsg.validId
	handler = qanda.popResponseHandler(who, handlerId)
	if handler:
		handler.handle(who)

def rpcWalkToPosRequest(who, sceneId, x, y, responseFunc=None,):
	'''寻路到指定坐标
	'''
	if responseFunc:  # 需要回应
		isResponse = 1
		responseCheckFunc = functor(checkWalkToPosResponse, sceneId, x, y)
	else:  # 不需要回应
		isResponse = 0
		responseCheckFunc = None

	handlerId = qanda.setupResponseHandler(who, responseFunc, responseCheckFunc)
	msg = qanda_pb2.walkReq()
	msg.validId = handlerId
	msg.sceneId = sceneId
	msg.x = x
	msg.y = y
	msg.isResponse = isResponse
	
	who.endPoint.rpcWalkToPosRequest(msg)
	
def checkWalkToPosResponse(who, sceneId, x, y):
	'''检查寻路回应
	'''
	if who.sceneId != sceneId:
		return 0
	if not scene.isNearBy(who, (sceneId, x, y)):
		return 0
	return 1

#===============================================================================
# 选择框
#===============================================================================
def rpcSelectBoxResponse(who, reqMsg):
	'''选择框回应
	'''
	handlerId = reqMsg.validId
	selectNo = reqMsg.responseVal
	if selectNo <= 0:
		return
	handler = qanda.popResponseHandler(who, handlerId)
	if handler:
		handler.handle(who, selectNo)
		
def rpcSelectBoxRequest(who, responseFunc, content, **kwargs):
	'''弹出选择框
	'''
	handlerId = qanda.setupResponseHandler(who, responseFunc)
	msg = {
		"validId": handlerId,
		"content": content,
	}	
	msg.update(kwargs)
	
	who.endPoint.rpcSelectBoxRequest(**msg)

#===============================================================================
# 确认框
#===============================================================================
def rpcConfirmBoxResponse(who, reqMsg):
	'''确认框回应
	'''
	handlerId = reqMsg.validId
	yes = reqMsg.responseVal
	handler = qanda.popResponseHandler(who, handlerId)
	if handler:
		handler.handle(who, yes)

def rpcConfirmBoxRequest(who, responseFunc, content):
	'''弹出确认框
	'''
	handlerId = qanda.setupResponseHandler(who, responseFunc)
	msg = {
		"validId": handlerId,
		"content": content,
	}
	who.endPoint.rpcConfirmBoxRequest(**msg)

#===============================================================================
# 队伍确认框
#===============================================================================
def rpcTeamBoxRequest(teamObj, func, title, content, timeOut):
	'''弹出队伍确认框
	'''
	teamObj.confirmResponse = func
	confirmTimeOut = getattr(teamObj, "confirmTimeOut", 0)
	if (confirmTimeOut + 120) < getSecond():
		teamObj.confirmList = {}
	teamObj.confirmTimeOut = getSecond()
	msgObj = packTeamConfirmBoxReq(teamObj, title, content, timeOut)
	packetMsg = endPoint.makePacket("rpcTeamConfirmBoxRequest", msgObj)
	for pid in teamObj.getInTeamList():
		roleObj = getRole(pid)
		if roleObj:
			roleObj.endPoint.send(packetMsg)

def packTeamConfirmBoxReq(teamObj, title, content, timeOut):
	msgObj = qanda_pb2.confirmTeamBoxReq()
	msgObj.title = title
	msgObj.content = content
	msgObj.timeOut = timeOut
	msgObj.leader = teamObj.leader
	msgObj.memberList.extend(packMemberList(teamObj))
	return msgObj

def packMemberList(teamObj):
	confirmList = getattr(teamObj, "confirmList", {})

	memberListMsg = []
	for pid in teamObj.getInTeamList():
		roleObj = getRole(pid)
		memberMsg = qanda_pb2.member()
		memberMsg.roleId = pid
		memberMsg.shape = roleObj.shape
		memberMsg.name = roleObj.name
		memberMsg.level = roleObj.level
		memberMsg.school = roleObj.school
		memberMsg.state = teamObj.getState(pid)
		if pid in confirmList:
			memberMsg.confirm = True
		memberListMsg.append(memberMsg)
	return memberListMsg

def rpcTeamConfirmBoxResponse(who, reqMsg):
	'''组队确认框回应
	'''
	teamId = reqMsg.teamId
	confirm = reqMsg.responseVal
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	if teamId != teamObj.id:
		return
	confirmList = getattr(teamObj, "confirmList", {})
	memberList = teamObj.getInTeamList()
	if confirm:
		if who.id in confirmList:
			return
		confirmList[who.id] = True
		if not isTeamConfirmAll(confirmList, memberList):
			rpcTeamConfirmBoxChange(memberList, who.id)
			return
		rpcTeamConfirmBoxResult(memberList)
		func = teamObj.confirmResponse
		del teamObj.confirmResponse
		del teamObj.confirmList
		del teamObj.confirmTimeOut
		func()
	else:
		if who.id in confirmList:
			del teamObj.confirmList[who.id]
		del teamObj.confirmResponse
		tips = "#C04{}#n已取消了行动".format(who.name)
		rpcTeamConfirmBoxResult(memberList, tips)

def isTeamConfirmAll(confirmList, memberList):
	for pid in memberList:
		if pid not in confirmList:
			return False
	return True

def rpcTeamConfirmBoxResult(memberList, tips=""):
	for pid in memberList:
		roleObj = getRole(pid)
		if not roleObj:
			continue
		roleObj.endPoint.rpcTeamConfirmBoxResult()
		if tips:
			message.tips(roleObj, tips)

def rpcTeamConfirmBoxChange(memberList, roleid):
	for pid in memberList:
		roleObj = getRole(pid)
		if roleObj:
			roleObj.endPoint.rpcTeamConfirmBoxChange(roleid)

#===============================================================================
# 物品上交
#===============================================================================
def rpcPopPropsResponse(who, reqMsg):
	'''上交物品回应
	'''
	handlerId = reqMsg.validId
	propsList = {}
	for itemMsgObj in reqMsg.itemList:
		if itemMsgObj.amount < 1: # 数量有异常，放弃此上交
			return
		propsList[itemMsgObj.id] = itemMsgObj.amount

	handler = qanda.popResponseHandler(who, handlerId)
	if handler:
		handler.handle(who, propsList)
		
def rpcPopPropsRequest(who, responseFunc, title, propsIdList):
	'''上交物品请求
	'''
	responseCheckFunc = functor(checkPopPropsResponse, propsIdList)
	handlerId = qanda.setupResponseHandler(who, responseFunc, responseCheckFunc)
	msg = {
		"validId": handlerId,
		"title": title,
		"idList": propsIdList,
	}	
	who.endPoint.rpcPopPropsRequest(**msg)
	
def checkPopPropsResponse(who, propsList, propsIdList):
	'''检查上交的物品
	'''
	if not propsList:
		return False
	for propsId in propsList:
		if propsId not in propsIdList:
			return False
	return True


#===============================================================================
# 进度条
#===============================================================================
def rpcProgressBarResponse(who, reqMsg):
	'''进度条回应
	'''
	handlerId = reqMsg.validId
	isDone = reqMsg.responseVal
	handler = qanda.popResponseHandler(who, handlerId)
	if handler:
		handler.handle(who, isDone)
		
def rpcProgressBarRequest(who, responseFunc, title, icon, ti, brk):
	'''进度条请求
	'''
	handlerId = qanda.setupResponseHandler(who, responseFunc)
	msg = {
		"validId": handlerId,
		"title": title,
		"icon": icon,
		"time": ti,
		"brk": brk,
	}
	who.endPoint.rpcProgressBarRequest(**msg)
	

from common import *
from qanda.defines import *
import qanda
import scene
import re
import scene
import qanda_pb2
import message
