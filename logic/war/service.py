# -*- coding: utf-8 -*-
# 战斗服务
import endPoint
import war_pb2

class cService(war_pb2.terminal2main):

	@endPoint.result
	def rpcWarCmdPhy(self, ep, who, reqMsg): return rpcWarCmdPhy(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdMag(self, ep, who, reqMsg): return rpcWarCmdMag(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdSE(self, ep, who, reqMsg): return rpcWarCmdSE(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdItem(self, ep, who, reqMsg): return rpcWarCmdItem(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdDefend(self, ep, who, reqMsg): return rpcWarCmdDefend(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdProtect(self, ep, who, reqMsg): return rpcWarCmdProtect(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdSummon(self, ep, who, reqMsg): return rpcWarCmdSummon(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdEscape(self, ep, who, reqMsg): return rpcWarCmdEscape(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdCapture(self, ep, who, reqMsg): return rpcWarCmdCapture(who, reqMsg)
	
	@endPoint.result
	def rpcWarCmdDefaultMag(self, ep, who, reqMsg): return rpcWarSetDefaultMag(who, reqMsg)
	
	@endPoint.result
	def rpcWarLeaveWatch(self, ep, who, reqMsg): return rpcWarLeaveWatch(who, reqMsg)
	
	@endPoint.result
	def rpcWarEnterWatch(self, ep, who, reqMsg): return rpcWarEnterWatch(who, reqMsg)
	
	@endPoint.result
	def rpcWarDrawEnd(self, ep, who, reqMsg): return rpcWarDrawEnd(who, reqMsg)
	
	@endPoint.result
	def rpcWarChange(self, ep, who, reqMsg): return rpcWarChange(who, reqMsg)


#===============================================================================
# 下达出招指令
#===============================================================================
def checkSetCmd(who, reqMsg, cmdType):
	'''检查下达指令
	'''
	tmpMsg = str(reqMsg).replace("\n", ",")
	cmdTypeName = cmdTypeNameList[cmdType]
	
	args = {
		"targetIdx": reqMsg.target,
		"performId": reqMsg.pfId,
		"itemId": reqMsg.itemId,
	}
	
	warObj = who.inWar()
	if not warObj:
		return None, None, args
	if who.inWatchWar():
		message.debugClientMsg(who, "在观战中却下达了指令:%s" % tmpMsg)
		return None, None, args
	
	w = warObj.getWarrior(reqMsg.idx, False)
	if not w:
		message.debugClientMsg(who, "找不到战士，请确认自己在战斗中:%s" % tmpMsg)
		return None, None, args
	if warObj.turnState != TURN_STATE_READY:
		message.debugClientMsg(who, "%s下达指令:%s，却不在回合准备阶段" % (w.name, tmpMsg))
		return None, None, args
	if w.command: # 已下达了指令
		message.debugClientMsg(who, "%s重复下达指令:%s" % (w.name, tmpMsg))
		return None, None, args
	if not w.isRole() and who.warrior.petIdx != w.idx:  # 不是自己的宠物
		message.debugClientMsg(who, "宠物%s下达指令，但该宠物不是自己的:%s" % (w.name, tmpMsg))
		return None, None, args
	
	warObj.printDebugMsg("$type战士[%s]  --->下达%s指令:%s" % (w.name, cmdTypeName, tmpMsg), w)
	return warObj, w, args

def setCommand(who, warObj, w, cmdType, **args):
	'''下达指令
	'''
	if w.isRole() and warObj.isAutoFight(w) and cmdType == CMD_TYPE_MAG: # 自动战斗的玩家下达法术指令要特殊处理
		performId = w.getAutoPerform(args["performId"], args["targetIdx"])
		if performId == CMD_TYPE_PHY:
			cmdType = CMD_TYPE_PHY
			args["targetIdx"] = 0
			args["performId"] = 0
		elif performId != args["performId"]:
			args["targetIdx"] = 0
			args["performId"] = performId
	
	war.commands.setCommand(warObj, w, cmdType, **args)
	warObj.onSetRoleCommand(w)
	

def rpcWarCmdPhy(who, reqMsg):
	'''下达物理攻击(平砍)指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_PHY)
	if not w:
		return
	setCommand(who, warObj, w, CMD_TYPE_PHY, **args)

def rpcWarCmdMag(who, reqMsg):
	'''下达法术攻击指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_MAG)
	if not w:
		return
	setCommand(who, warObj, w, CMD_TYPE_MAG, **args)

def rpcWarCmdSE(who, reqMsg):
	'''下达特技攻击指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_SE)
	if not w:
		return
	if not w.isRole(): # 只有玩家才可以使用特技
		tmpMsg = str(reqMsg).replace("\n", ",")
		message.debugClientMsg(who, "只有玩家才可以下达特技指令:%s" % tmpMsg)
		return
	setCommand(who, warObj, w, CMD_TYPE_SE, **args)

def rpcWarCmdItem(who, reqMsg):
	'''下达使用物品指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_ITEM)
	if not w:
		return
	setCommand(who, warObj, w, CMD_TYPE_ITEM, **args)

def rpcWarCmdDefend(who, reqMsg):
	'''下达防御指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_DEFEND)
	if not w:
		return
	setCommand(who, warObj, w, CMD_TYPE_DEFEND, **args)

def rpcWarCmdProtect(who, reqMsg):
	'''下达保护指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_PROTECT)
	if not w:
		return
	setCommand(who, warObj, w, CMD_TYPE_PROTECT, **args)

def rpcWarCmdSummon(who, reqMsg):
	'''下达召唤宠物指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_SUMMON)
	if not w:
		return
	if not w.isRole():  # 只有玩家才可以召唤
		tmpMsg = str(reqMsg).replace("\n", ",")
		message.debugClientMsg(who, "只有玩家才下达召唤指令:%s" % tmpMsg)
		return
	setCommand(who, warObj, w, CMD_TYPE_SUMMON, **args)

def rpcWarCmdEscape(who, reqMsg):
	'''下达逃跑指令
	'''
	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_ESCAPE)
	if not w:
		return
	setCommand(who, warObj, w, CMD_TYPE_ESCAPE, **args)
	
def rpcWarCmdCapture(who, reqMsg):
	'''下达捕捉指令
	'''
	pass # 屏蔽不使用
# 	warObj, w, args = checkSetCmd(who, reqMsg, CMD_TYPE_CAPTURE)
# 	if not w:
# 		return
# 	if not w.isRole():  # 只有玩家才可以捕捉
# 		tmpMsg = str(reqMsg).replace("\n", ",")
# 		message.debugClientMsg(who, "只有玩家才可以下达捕捉指令:%s" % tmpMsg)
# 		return
# 	setCommand(who, warObj, w, CMD_TYPE_CAPTURE, **args)



#===============================================================================
# 其它相关
#===============================================================================
def checkReqMsg(who, reqMsg):
	if not who.inWar():
		return None, None
	
	warObj = who.war
	w = warObj.getWarrior(reqMsg.idx, False)
	if not w:
		return None, None
		
	return warObj, w

def rpcWarSetDefaultMag(who, reqMsg):
	'''设置默认法术指令
	'''
	pass
# 	warObj, w = checkReqMsg(who, reqMsg)
# 	if not w:
# 		return
# 
# 	targetIdx = reqMsg.idx
# 	performId = reqMsg.pfId
# 	if targetIdx == w.idx: # 玩家自己
# 		obj = who
# 		targetW = w
# 	elif targetIdx == w.petIdx: # 宠物
# 		petObj = who.petCtn.getItem(w.id)
# 		if petObj:
# 			obj = petObj
# 		else:
# 			return
# 		
# 		sw = warObj.getWarrior(targetIdx, False)
# 		if sw:
# 			targetW = sw
# 		else:
# 			return
# 	else:
# 		return
# 			
# 	obj.setDefaultPerform(performId)
# 	w.setDefaultPerform(performId)

def rpcWarLeaveWatch(who, reqMsg):
	'''退出观战
	'''
	warObj = who.inWatchWar()
	if not warObj:
		message.debugClientMsg(who, "不在观战中，请检查是否有bug")
		return
	
	w = who.warrior
	warObj.kickWatcher(w)
	
def rpcWarEnterWatch(who, reqMsg):
	'''进入观战
	'''
	if who.inEscort():
		message.tips(who, "运镖中不能观战")
		return
	if who.inWar():
		message.debugClientMsg(who, "已在参战或观战中，请检查是否有bug")
		return
		
	targetId = reqMsg.iValue
	targetObj = getRole(targetId)
	if not targetObj:
		message.tips(who, "对方已下线")
		return
	
	warObj = targetObj.inWar()
	if not warObj:
		message.tips(who, "对方已退出战斗")
		return
	if hasattr(warObj, "doneEnd"):
		return
	
	teamObj = who.inTeam()
	if teamObj:
		if not teamObj.isLeader(who.id): # 在队队员不能点击观战
			return
		warObj.addTeamWatch(teamObj, targetObj.warrior.side)
	else:
		warObj.addWatch(who, targetObj.warrior.side)
		
def rpcWarDrawEnd(who, reqMsg):
	'''客户端回合动画播放结束
	'''
	warObj = who.inWar()
	if not warObj:
		return
	if hasattr(warObj, "doneEnd"):
		return
	
	w = who.warrior
	if not w.isRole():
		return
	warObj.setClientDrawEnd(w)
	
def rpcWarChange(who, reqMsg):
	'''修改战斗信息
	'''
	warObj = who.inWar()
	if not warObj:
		return
	
	for attrObj, attrVal in reqMsg.ListFields():
		attrName = attrObj.name
		if attrName == "autoFight":
			who.setAutoFight(attrVal)

from common import *
from war.defines import *
import war.commands
import message
import war