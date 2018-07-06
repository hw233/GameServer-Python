# -*- coding: utf-8 -*-
'''聊天相关服务: 聊天服<--->客户端
'''
from chatService.defines import *
import terminal_chat_pb2
import endPoint

class cService(terminal_chat_pb2.terminal2chat):

	@endPoint.result
	def rpcChatUp(self, ep, senderObj, reqMsg):return rpcChatUp(ep, senderObj, reqMsg)

	@endPoint.result
	def rpcBanChannelReq(self, ep, senderObj, reqMsg):return rpcBanChannelReq(ep, senderObj, reqMsg)

	@endPoint.result
	def rpcBanChannelSet(self, ep, senderObj, reqMsg):return rpcBanChannelSet(ep, senderObj, reqMsg)

	# @endPoint.result
	# def rpcAudioReq(self, ep, senderObj, reqMsg):return rpcAudioReq(ep, senderObj, reqMsg)

	@endPoint.result
	def rpcHeartbeat(self, ep, senderObj, reqMsg):return rpcHeartbeat(ep, senderObj, reqMsg)

def rpcHeartbeat(ep, senderObj, reqMsg):
	return True

def rpcChatUp(ep, senderObj, reqMsg):
	'''发送聊天信息
	'''
	channelId = reqMsg.channelId
	content = reqMsg.content
	isAudio = reqMsg.isAudio
	if not content:
		message.tips(senderObj, "请输入要说的话")
		return
	if channelId == CHANNEL_TEAM and not senderObj.teamId:
		message.tips(senderObj, "你没加入任何队伍，请加入后再发言")
		return
	if channelId == CHANNEL_GUILD:
		if not senderObj.guildId:
			message.tips(senderObj, "你没加入任何仙盟，请加入后再发言")
			return
		elif senderObj.guildBan:
			minute = (senderObj.guildBan - getSecond()) / 60
			if minute > 0:
				message.tips(senderObj, "你的禁言还剩#C04{}分钟#n".format(minute))
				return
	if channelId == CHANNEL_FIGHT and not senderObj.warId:
		message.tips(senderObj, "你不在战斗中，不可在战斗频道中发言")
		return
	if not doChannelCost(senderObj, channelId, content):
		return

	content	= trie.fliter(content)
	msg = {
		"channelId": channelId,
		"content": content,
		"isAudio": isAudio,
	}
	if isAudio:
		handleAudio(channelId, reqMsg.audioIdx, reqMsg.audioLen, msg)
	doChannel(senderObj, channelId, msg)

def doChannelCost(senderObj, channelId, content):
	'''发言检查和消耗
	'''
	limitData = getLimitData(senderObj, channelId)
	if not limitData:
		return 0
	
	limitLen = limitData.get("内容长度")
	if limitLen and calLenForWord(content) > limitLen:
		message.tips(senderObj, "发言内容太多啦，请分开两次发言")
		return 0
	
	limitInterval = limitData.get("时间间隔")
	if limitInterval:
		if not hasattr(senderObj, "lastTimeList"):
			senderObj.lastTimeList = {}
		if channelId not in senderObj.lastTimeList:
			senderObj.lastTimeList[channelId] = 0

		lastTime = senderObj.lastTimeList[channelId]
		leftTime = limitInterval - (getSecond() - lastTime)
		if leftTime > 0:
			message.tips(senderObj, "发言太频密，还有#C04%d秒#n可发言" % leftTime)
			return 0
		
	limitHuoli = limitData.get("活力")
	if limitHuoli:
		channelName = getChannelName(channelId)
		bFail, msgObj = chatService.getMainEP().rpcCostHuoli(senderObj.id, limitHuoli)
		if bFail or not msgObj.bValue:
			message.tips(senderObj, "活力不足，无法在#C04%s#n发言" % channelName)
			return 0
	
	if limitInterval:
		senderObj.lastTimeList[channelId] = getSecond()
		
	return 1
		
def getLimitData(senderObj, channelId):
	'''获取限制数据
	'''
	data = channelData.getData(channelId)
	if not data:
		return None
	
	limitData = {}
	level = senderObj.level
	for k,v in data.iteritems():
		if isinstance(v, str):
			if "lv" in v:
				v = v.replace("lv", str(level))
			v = int(eval(v))
		limitData[k] = v

	return limitData

def doChannel(senderObj, channelId, msg):
	msgObj = packReceiveMsg(senderObj, msg)
	if channelId in (CHANNEL_WORLD, CHANNEL_SYS_ANNOUNCE, CHANNEL_SYS_MESSAGE):
		broadcastAll(senderObj, msgObj, channelId)
	else:
		if channelId in roleIdsGetHandler:
			handler = roleIdsGetHandler[channelId]
			roleIdList = handler(senderObj)
		else:
			if msg.get("targetId"): # 系统发送的消息
				targetId = msg["targetId"]
			else:
				attrName = channelId2AttrName[channelId]
				targetId = getattr(senderObj, attrName)
			roleIdList = chatService.gChannelMgr.getRoleIdList(channelId, targetId)

		if roleIdList:
			broadcastByRoleIds(senderObj, msgObj, channelId, roleIdList)

def roleIdsGetCurrent(senderObj):
	'''当前频道
	'''
	# 暂时先这样
	roleIdList = []
	sceneId = senderObj.sceneId
	for targetSender in chatService.getAllRoleSenderList():
		if targetSender.sceneId != sceneId:
			continue
		if targetSender.warId: # 战斗中的不发
			continue
		roleIdList.append(targetSender.id)
	return roleIdList

def roleIdsGetTeamMake(senderObj):
	'''组队频道
	'''
	roleIdList = []
	level = senderObj.fastChatLevel
	for targetSender in chatService.getAllRoleSenderList():
		if targetSender.teamId:  #有队伍的不用发
			continue
		if targetSender.level < level:
			continue
		roleIdList.append(targetSender.id)
	return roleIdList

def roleIdsGetGuildAnnounce(senderObj):
	'''仙盟公告频道
	'''
	roleIdList = []
	for targetSender in chatService.getAllRoleSenderList():
		if targetSender.guildId: # 有仙盟的不发
			continue
		roleIdList.append(targetSender.id)
	return roleIdList

# 获取发送的角色id列表的处理列表
roleIdsGetHandler = {
	CHANNEL_CURRENT: roleIdsGetCurrent, # 当前频道
	CHANNEL_TEAM_MAKE:roleIdsGetTeamMake, # 组队频道
	CHANNEL_GUILD_ANNOUNCE:roleIdsGetGuildAnnounce, # 仙盟公告频道
}


def packReceiveMsg(senderObj, msg):
	msgObj = terminal_chat_pb2.receiveMsg()
	msgObj.sender.CopyFrom(senderObj.getMsg())
	msgObj.channelId = msg["channelId"]
	msgObj.content = msg["content"]
	msgObj.isAudio = msg.get("isAudio", 0)
	msgObj.roll = msg.get("roll", 0)
	audioInfo = msg.get("audioInfo", None)
	if audioInfo:
		msgObj.audio.CopyFrom(audioInfo)
	fastChatInfo = msg.get("fastChat")
	if fastChatInfo:
		msgObj.fastChat.CopyFrom(fastChatInfo)
	return msgObj

def broadcastAll(senderObj, msgObj, channelId):
	'''广播给所有角色
	'''
	packetData = endPoint.makePacket("rpcChatDown", msgObj)
	for targetSender in chatService.getAllRoleSenderList():
		ep = targetSender.endPoint
		if not ep: # 链接断开时，ep判断为False
			continue
		if targetSender.isChannelBaned(channelId, senderObj.id):
			continue
		ep.send(packetData)

def broadcastByRoleIds(senderObj, msgObj, channelId, roleIdList):
	'''根据角色id进行组播
	'''
	packetData = endPoint.makePacket("rpcChatDown", msgObj)
	for roleId in roleIdList:
		targetSender = chatService.getSender(roleId)
		if not targetSender:
			continue
		ep = targetSender.endPoint
		if not ep: # 链接断开时，ep判断为False
			continue
		if targetSender.isChannelBaned(channelId, senderObj.id):
			continue
		ep.send(packetData)
		
def rpcBanChannelReq(ep, senderObj, reqMsg):
	'''请求屏蔽的频道
	'''
	msg = terminal_chat_pb2.banChannelMsg()
	msg.channelIdList.extend(senderObj.channelBanList)
	senderObj.endPoint.rpcBanChannelRes(msg)
		
def rpcBanChannelSet(ep, senderObj, reqMsg):
	'''设置屏蔽的频道
	'''
	senderObj.channelBanList = reqMsg.channelIdList

# def rpcAudioReq(ep, senderObj, reqMsg):
# 	'''请求语音信息
# 	'''
# 	idx = reqMsg.audioIdx
# 	audioObj = chatService.gAudioMgr.getAudio(idx)
# 	if not audioObj:
# 		message.tips(senderObj, "不存在此语音信息")
# 		return
# 	senderObj.endPoint.rpcAudioRes(audioObj.getMsg())

def handleAudio(channelId, iIdx, iLen, dMsg):
	audioObj = chatService.gAudioMgr.addAudio(channelId, iIdx, iLen)
	if audioObj:
		dMsg["audioInfo"] = audioObj


from common import *
from chatService.defines import *
import chatService
import channelData
import message
import trie