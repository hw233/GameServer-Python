# -*- coding: utf-8 -*-
'''成就服务
'''
import achv_pb2
import endPoint

class cService(achv_pb2.terminal2main):	
	@endPoint.result
	def rpcAchvShare(self, ep, who, reqMsg): return rpcAchvShare(who, reqMsg)


def getAchvMsg(achvObj):
	msg = achv_pb2.achvMsg()
	msg.id = achvObj.id
	msg.isDone = achvObj.isDone()
	msg.doneTime = achvObj.fetch("doneTime")

	if achvObj.kind == ACHV_KIND_PROG:
		msg.progress = achvObj.fetch("progress")

	elif achvObj.kind == ACHV_KIND_COND:
		condDoneList = achvObj.fetch("condDoneList", {})
		msg.condDoneList.extend(condDoneList.keys())

	return msg

def rpcAchvAdd(who, achvObj):
	'''增加成就
	'''
	msg = getAchvMsg(achvObj)
	who.endPoint.rpcAchvAdd(msg)

def rpcAchvDelete(who, achvId):
	'''删除成就
	'''
	who.endPoint.rpcAchvDelete(achvId)

def rpcAchvDone(who, achvObj):
	'''成就达成
	'''
	msg = getAchvMsg(achvObj)
	who.endPoint.rpcAchvDone(msg)

def rpcAchvChangeProg(who, achvObj):
	'''刷新成就进度
	'''
	msg = getAchvMsg(achvObj)
	who.endPoint.rpcAchvChangeProg(msg)

def rpcAchvChangeCond(who, achvObj):
	'''刷新成就已达成条件
	'''
	msg = getAchvMsg(achvObj)
	who.endPoint.rpcAchvChangeCond(msg)

def rpcAchvShare(who, reqMsg):
	'''分享成就
	'''
	achvId = reqMsg.id
	channelId = reqMsg.channelId

	achvObj = who.achvCtn.getItem(achvId)
	if not achvObj or not achvObj.isDone():
		#成就没达成
		return
	#频道
	if channelId not in (CHANNEL_WORLD, CHANNEL_SCHOOL, CHANNEL_GUILD, CHANNEL_CURRENT):
		return
	#仙盟频道
	if channelId == CHANNEL_GUILD:
		oGuild = who.getGuildObj()
		if not oGuild:
			message.tips(who, "你没有加入仙盟")
			return

	targetId = 0
	if channelId == CHANNEL_SCHOOL:
		targetId = who.school
	elif channelId == CHANNEL_GUILD:
		targetId = who.getGuildId()

	msg = {
			"channelId": channelId,
			"content": "#L2<{},10,0,{}>*[{}]*02#n".format(who.id, achvObj.id, achvObj.name),
			"senderId": who.id,
			"targetId": targetId,
		}

	pid = who.id
	bFail, resMsg = mainService.getChatEP().rpcShareAchv(**msg)
	who = getRole(pid)
	if not who:
		return
	if bFail:
		return

	if resMsg.bValue:
		message.tips(who, "已在频道分享成就")

def rpcAchvHyperlink(who, targetRole, achvId, *args):
	'''查看成就超链接
	'''
	if not targetRole:
		message.tips(who, "该链接已经失效")
		return
	# if who.id == targetRole.id:
	# 	return
	achvObj = targetRole.achvCtn.getItem(achvId)
	if not achvObj or not achvObj.isDone():
		message.tips(who, "该链接已经失效")
		return
	msg = {	
		"id" : achvObj.id,
		"doneTime" : achvObj.fetch("doneTime"),
	}
	
	who.endPoint.rpcAchvHyperlink(**msg)





from achv.defines import *
from chatService.defines import *
from common import *
import message
import mainService
