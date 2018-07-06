# -*- coding: utf-8 -*-

def tips(target, msg):
	'''渐隐式提示
	'''
	if not isinstance(target, (dict, list, tuple)):
		targetList = [target, ]
	else:
		targetList = target

	for pid in targetList:
		if isinstance(pid, (int, long)):
			obj = getRole(pid)
		else:
			obj = pid
		if obj:
			obj.endPoint.rpcTips(msg)
			
def message(target, msg):
	'''信息提示，显示在系统频道
	'''
	if not isinstance(target, (dict, list, tuple)):
		targetList = [target, ]
	else:
		targetList = target

	for pid in targetList:
		if isinstance(pid, (int, long)):
			obj = getRole(pid)
		else:
			obj = pid
		if obj:
			obj.endPoint.rpcMessage(msg)
			
def dialog(target, msg):
	'''对白框
	'''
	if isinstance(target, (int, long)):
		obj = getRole(target)
	else:
		obj = target
	obj.endPoint.rpcModalDialog(msg)
	
def npcSayByArgs(target, content, name="", shape=0, npcId=0):
	'''指定参数的npc对话框
	'''
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target

	msg = {
		"npcId": npcId,
		"shape": shape,
		"name": name,
		"content": content,
	}
	roleObj.endPoint.rpcNpcSay(**msg)
			
def inputBox(who, responseFunc, title, content, limitType=0, limitLength=0):
	'''弹出输入框
	'''
	qanda.service.rpcInputBoxRequest(who, responseFunc, title, content, limitType, limitLength)

def selectBoxByArgs(target, content, name="", shape=0, npcId=0):
	'''指定参数的选择框
	'''
	if isinstance(target, (int, long)):
		obj = getRole(target)
	else:
		obj = target
	
	msg = {"sQuestion": content}
	if name:
		msg["sTitle"] = name
	if shape:
		msg["iShape"] = shape
	if npcId:
		msg["npcId"] = npcId
	
	bFail, resMsg = obj.endPoint.rpcSelectBox(**msg)
	if bFail:
		return None
	return resMsg.iValue

def selectBox(target, content, npcObj):
	'''带有npc的选择框
	'''
	name = npcObj.name
	shape = npcObj.shape
	if hasattr(npcObj, "triggerNpc"):
		npcId = npcObj.id
		del npcObj.triggerNpc
	else:
		npcId = 0
	return selectBoxByArgs(target, content, name, shape, npcId)

def selectBoxByArgsNew(target, responseFunc, content, **kwargs):
	'''指定参数的选择框
	'''
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target
	qanda.service.rpcSelectBoxRequest(roleObj, responseFunc, content, **kwargs)

def selectBoxNew(target, responseFunc, content, npcObj):
	'''带有npc的选择框
	responseFunc: 客户端返回时的处理函数 
	'''
	if hasattr(npcObj, "triggerNpc"):
		npcId = npcObj.id
		del npcObj.triggerNpc
	else:
		npcId = 0

	kwargs = {
		"title": npcObj.name,
		"shape": npcObj.shape,
		"npcId": npcId,
	}
	return selectBoxByArgsNew(target, responseFunc, content, **kwargs)

def confirmBox(target, msg):
	'''确认框
	'''
	if isinstance(target, (int, long)):
		obj = getRole(target)
	else:
		obj = target
	bFail, resMsg = obj.endPoint.rpcConfirmBox(msg)
	if bFail:
		return None
	return resMsg.iValue

def confirmBoxNew(target, responseFunc, content):
	'''确认框
	responseFunc: 客户端返回时的处理函数 
	'''
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target
	qanda.service.rpcConfirmBoxRequest(roleObj, responseFunc, content)
	
def popPetUI(target, responseFunc, title, petIdList):
	'''弹出上交宠物界面
	responseFunc: 客户端返回时的处理函数 
	'''
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target
		
	qanda.service.rpcPropsRequest(roleObj, responseFunc, title, petIdList)

def popPropsUI(target, responseFunc, title, propsIdList):
	'''弹出上交物品界面
	responseFunc: 客户端返回时的处理函数 
	'''
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target
		
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target
		
	qanda.service.rpcPopPropsRequest(roleObj, responseFunc, title, propsIdList)

def progressBar(target, responseFunc, title, icon, ti, brk):
	'''进度条
	'''
	if isinstance(target, (int, long)):
		roleObj = getRole(target)
	else:
		roleObj = target
	qanda.service.rpcProgressBarRequest(roleObj, responseFunc, title, icon, ti, brk)

def cashLackBox(target, msg):
	'''银币不足框
	'''
	if isinstance(target, (int, long)):
		who = getRole(target)
	else:
		who = target

	bFail, resMsg = who.endPoint.rpcCashLackBox(msg)
	if bFail:
		return None
	return resMsg.iValue

def tradeCashLackBox(target, msg):
	'''元宝不足框
	'''
	if isinstance(target, (int, long)):
		who = getRole(target)
	else:
		who = target

	bFail, resMsg = who.endPoint.rpcTradeCashLackBox(msg)
	if bFail:
		return None
	return resMsg.iValue

def schoolMessage(schoolId, content):
	'''门派传闻
	'''
	msg = {
		"channelId": CHANNEL_SCHOOL,
		"content": content,
		"targetId": schoolId,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)
	
def teamMessage(teamId, content):
	'''队伍传闻
	'''
	msg = {
		"channelId": CHANNEL_TEAM,
		"content": content,
		"targetId": teamId,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)
	
def guildMessage(guildId, content):
	'''仙盟传闻
	'''
	msg = {
		"channelId": CHANNEL_GUILD,
		"content": content,
		"targetId": guildId,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)
	
def guildAnnounce(guildId, content):
	'''仙盟公告
	'''
	msg = {
		"channelId": CHANNEL_GUILD_ANNOUNCE,
		"content": content,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)
	
def sysAnnounce(content, roll=0):
	'''系统公告
	'''
	msg = {
		"channelId": CHANNEL_SYS_ANNOUNCE,
		"content": content,
		"roll": roll,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)

def sysMessage(content, roll=0):
	'''系统传闻
	'''
	msg = {
		"channelId": CHANNEL_SYS_MESSAGE,
		"content": content,
		"roll": roll,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)

def sysAnnounceRoll(content):
	'''系统公告并滚动
	'''
	sysAnnounce(content, 1)

def sysMessageRoll(content):
	'''系统传闻并滚动
	'''
	sysMessage(content, 1)

def sysRoll(content):
	'''滚动公告
	'''
	sysAnnounce(content, 2)
	
def sysRoleRoll(roleId, content):
	'''玩家滚动公告
	'''
	if isinstance(roleId, (int, long)):
		who = getRole(roleId)
	else:
		who = roleId
		
	content = "#N({},{},)#n{}".format(who.id, who.name, content)
	sysRoll(content)
	
def worldMessage(content):
	'''世界传闻
	'''
	msg = {
		"channelId": CHANNEL_WORLD,
		"content": content,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)
	
def worldRoleMessage(roleId, content):
	'''玩家世界传闻
	'''
	if isinstance(roleId, (int, long)):
		pass
	else:
		who = roleId
		roleId = who.id

	msg = {
		"channelId": CHANNEL_WORLD,
		"content": content,
		"senderId": roleId,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)

def currentRoleMessage(roleId, content):
	'''玩家当前传闻
	'''
	if isinstance(roleId, (int, long)):
		pass
	else:
		who = roleId
		roleId = who.id

	msg = {
		"channelId": CHANNEL_CURRENT,
		"content": content,
		"senderId": roleId,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)

def guildRoleMessage(roleId, guildId, content):
	'''玩家仙盟传闻
	'''
	msg = {
		"channelId": CHANNEL_GUILD,
		"content": content,
		"targetId": guildId,
		"senderId": roleId,
	}
	mainService.getChatEP().rpcSysSendMsg(**msg)

def debugClientMsg(pid, msg):
	if not config.SHOW_EXCEPTION:
		return

	msg = "请通知客户端程序员\n" + msg
	dialog(pid, msg)
	writeLog("client/bug", msg)

def teamConfirmBox(teamObj,func,title,content,timeOut=60):
	qanda.service.rpcTeamBoxRequest(teamObj,func,title,content,timeOut)

	

from common import *
from chatService.defines import *
import npc.object
import qanda.service
import mainService
import config
