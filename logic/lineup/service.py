# -*- coding: utf-8 -*-
'''阵法服务
'''
import endPoint
import lineup_pb2

class cService(lineup_pb2.terminal2main):

	@endPoint.result
	def rpcLineupLearn(self, ep, who, reqMsg): return rpcLineupLearn(who, reqMsg)
	
	@endPoint.result
	def rpcLineupUpgrade(self, ep, who, reqMsg): return rpcLineupUpgrade(who, reqMsg)

	@endPoint.result
	def rpcEyeUse(self, ep, who, reqMsg): return rpcEyeUse(who, reqMsg)
	
	@endPoint.result
	def rpcEyeChange(self, ep, who, reqMsg): return rpcEyeChange(who, reqMsg)

def rpcLineupLearn(who, reqMsg):
	'''学习阵法
	'''
	lineupId = reqMsg.iValue
	lineup.upgrade.learn(who, lineupId)
		
def rpcLineupUpgrade(who, reqMsg):
	'''提升阵法
	'''
	lineupId = reqMsg.lineupId
	propsIdList = {}
	for obj in reqMsg.propsList:
		propsIdList[obj.id] = obj.amount
	
	lineupObj = who.lineupCtn.getItem(lineupId)
	if not lineupObj:  # 身上没有此阵法
		return
	lineup.upgrade.upgrade(who, lineupObj, propsIdList)

def rpcEyeUse(who, reqMsg):
	'''使用阵眼
	'''
	# if who.level <50:
	# 	return
	eyeId = reqMsg.eyeId
	eyeObj = who.eyeCtn.getItem(eyeId)
	if not eyeObj:
		return
	
	lineupObj = who.lineupCtn.getItem(eyeObj.getNo())
	if not lineupObj:
		message.tips(who,"没有可以装备的阵法")
		return
	
	lineupObj.setEyeObj(eyeObj)

def rpcEyeChange(who, reqMsg):
	'''阵眼变幻
	'''
	# if who.level <50:
	# 	return
	eyeId = reqMsg.eyeId
	eyeObj = who.eyeCtn.getItem(eyeId)
	if not eyeObj:
		return

	lineup.upgrade.eyeChange(who,eyeObj)

#===============================================================================
# 服务端发往客户端
#===============================================================================
def packetLineupMsg(lineupObj):
	'''打包阵法信息
	'''
	msgObj = lineup_pb2.lineupMsg()
	msgObj.lineupId = lineupObj.id
	msgObj.level = lineupObj.level
	msgObj.exp = lineupObj.getExp()
	msgObj.eyeId = lineupObj.getEyeId()
	return msgObj

def packetEyeMsg(eyeObj):
	'''打包阵眼信息
	'''
	skillListMsg = packetSkillListMsg(eyeObj)
	
	msgObj = lineup_pb2.eyeMsg()
	msgObj.eyeId = eyeObj.id
	msgObj.eyeNo = eyeObj.getNo()
	msgObj.speRatio = eyeObj.getSpeRatio()
	msgObj.skillList.CopyFrom(skillListMsg)
	msgObj.isStar = eyeObj.isStar()
	msgObj.isUse = eyeObj.isUse()
	msgObj.stallCD = eyeObj.getStallCD()
	return msgObj

def packetSkillListMsg(eyeObj):
	'''打包阵眼技能信息
	'''
	skillIdList = []
	for skillId, skillObj in eyeObj.getSkillListByOrder():
		skillIdList.append(skillId)
	
	msgObj = lineup_pb2.skillListMsg()
	msgObj.skillIdList.extend(skillIdList)
	return msgObj
	
def rpcLineupList(who):
	'''发送阵法列表
	'''
	currentLineupObj = who.buddyCtn.getCurrentLineup()
	if currentLineupObj:
		currentLineupId = currentLineupObj.id
	else:
		currentLineupId = 0
	
	lineupList = []
	for lineupObj in who.lineupCtn.getAllValues():
		lineupMsg = packetLineupMsg(lineupObj)
		lineupList.append(lineupMsg)

	eyeList = []
	for eyeObj in who.eyeCtn.getAllValues():
		eyeMsg = packetEyeMsg(eyeObj)
		eyeList.append(eyeMsg)
		
	msgObj = lineup_pb2.lineupListMsg()
	msgObj.curLineupId = currentLineupId
	msgObj.lineupList.extend(lineupList)
	msgObj.eyeList.extend(eyeList)
	who.endPoint.rpcLineupList(msgObj)

def rpcLineupAdd(who, lineupObj):
	'''增加阵法
	'''
	msgObj = packetLineupMsg(lineupObj)
	who.endPoint.rpcLineupAdd(msgObj)
	
def rpcLineupDelete(who, lineupId):
	'''删除阵法
	'''
	who.endPoint.rpcLineupDelete(lineupId)

def rpcLineupMod(who, lineupObj, *attrNameList):
	'''修改阵法
	'''
	msg = {}
	msg["lineupId"] = lineupObj.id
	
	for attrName in attrNameList:
		attrVal = getValByName(lineupObj, attrName)
		msg[attrName] = attrVal
	
	who.endPoint.rpcLineupMod(**msg)

def rpcEyeAdd(who, eyeObj):
	'''增加阵眼
	'''
	msgObj = packetEyeMsg(eyeObj)
	who.endPoint.rpcEyeAdd(msgObj)
	
def rpcEyeDelete(who, eyeId):
	'''删除阵眼
	'''
	who.endPoint.rpcEyeDelete(eyeId)

def rpcEyeMod(who, eyeObj, *attrNameList):
	'''修改阵眼
	'''
	msg = {}
	msg["eyeId"] = eyeObj.id
	
	for attrName in attrNameList:
		if attrName == "skillList":
			attrVal = packetSkillListMsg(eyeObj)
		else:
			attrVal = getValByName(eyeObj, attrName)
		msg[attrName] = attrVal
	
	who.endPoint.rpcEyeMod(**msg)
	

from common import *
import lineup
import lineup.upgrade
import message