# -*- coding: utf-8 -*-
import main_chat_pb2
import endPoint

class cService(main_chat_pb2.main2chat):
	@endPoint.result
	def rpcHelloChat_iAmMain(self, ep, ctrlr, reqMsg):return rpcHelloChat_iAmMain(ep, ctrlr, reqMsg)
	
	@endPoint.result
	def rpcRegisterRole(self, ep, ctrlr, reqMsg):return rpcRegisterRole(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcUnRegisterRole(self, ep, ctrlr, reqMsg):return rpcUnRegisterRole(ep, ctrlr, reqMsg)
	
	@endPoint.result
	def rpcUpdateRole(self, ep, ctrlr, reqMsg):return rpcUpdateRole(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcSysSendMsg(self, ep, ctrlr, reqMsg):return rpcSysSendMsg(ep, ctrlr, reqMsg)
	
	@endPoint.result
	def rpcHotUpdate(self, ep, ctrlr, reqMsg):return rpcHotUpdate(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcFastChat(self, ep, ctrlr, reqMsg):return rpcFastChat(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcModFastChat(self, ep, ctrlr, reqMsg):return rpcModFastChat(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcDelFastChat(self, ep, ctrlr, reqMsg):return rpcDelFastChat(ep, ctrlr, reqMsg)
	
	@endPoint.result
	def rpcBroadcastAnswerQuick(self, ep, ctrlr, reqMsg):return rpcBroadcastAnswerQuick(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcShareAchv(self, ep, ctrlr, reqMsg):return rpcShareAchv(ep, ctrlr, reqMsg)

	@endPoint.result
	def rpcUpdateBlack(self, ep, ctrlr, reqMsg):return rpcUpdateBlack(ep, ctrlr, reqMsg)

def rpcHelloChat_iAmMain(ep, ctrlr, reqMsg):
	print "chatService.service4terminal"
	return True
	
def rpcRegisterRole(ep, ctrlr, reqMsg):
	'''注册角色
	'''
	epId = reqMsg.epId
	roleMsg = reqMsg.roleMsg
	roleId = roleMsg.roleId

	ep = chatService.gEndPointKeeper.getObj(epId)
	if not ep:
		print "rpcRegisterRole被call,没有找到iConnId={}".format(epId)
		return
	
	ep.setAssociativeRole(roleId)
	
	data = {}
	for obj, attrVal in roleMsg.ListFields():
		data[obj.name] = attrVal

	senderObj = chatService.getSender(roleId)
	if senderObj:
		senderObj.update(data)
	else:
		chatService.newSender(roleId, data)
	
def rpcUnRegisterRole(ep, ctrlr, reqMsg):
	'''注销角色
	'''
	roleId = reqMsg.iValue
	senderObj = chatService.getSender(roleId)
	if not senderObj:
		return
	senderObj.release()
	if senderObj.endPoint:
		senderObj.endPoint.resetAssociativeRole()
		
def rpcUpdateRole(ep, ctrlr, reqMsg):
	'''更新角色信息
	'''
	roleId = reqMsg.roleId
	senderObj = chatService.getSender(roleId)
	if not senderObj:
		return
	
	data = {}
	for obj, attrVal in reqMsg.ListFields():
		data[obj.name] = attrVal
	senderObj.update(data)
	
def rpcSysSendMsg(ep, ctrlr, reqMsg):
	'''系统发送的消息
	'''
	msg = {}
	for obj, val in reqMsg.ListFields():
		msg[obj.name] = val

	channelId = msg["channelId"]
	if msg.get("senderId"): # 玩家通过系统发的
		senderObj = chatService.getSender(msg["senderId"])
	else:
		senderObj = chatService.getSysSender()
	if senderObj:
		chatService.service4terminal.doChannel(senderObj, channelId, msg)
	
def rpcHotUpdate(ep, ctrlr, reqMsg):
	import hotUpdate
	modPath = reqMsg.sValue
	hotUpdate.update(modPath)

def rpcFastChat(ep, ctrlr, reqMsg):
	'''一键喊话
	'''
	channelId = reqMsg.channelId
	content = reqMsg.content
	roleId = reqMsg.roleId
	fastChat = reqMsg.fastChat
	msg = {
		"channelId": channelId,
		"content": content,
		"fastChat":packFastChatMsg(fastChat),
	}
	senderObj = chatService.getSender(roleId)
	senderObj.fastChatLevel = teamTargetData.getConfig(fastChat.task,"活动等级")
	chatService.service4terminal.doChannel(senderObj, channelId, msg)

def rpcModFastChat(ep, ctrlr, reqMsg):
	'''修改一键喊话
	'''
	broadcastAll("rpcModFastChat", packFastChatMsg(reqMsg))

def rpcDelFastChat(ep, ctrlr, reqMsg):
	'''删除一键喊话
	'''
	broadcastAll("rpcDelFastChat", reqMsg)

def packFastChatMsg(fastChat):
	msgObj = terminal_chat_pb2.fastChatInfo()
	msgObj.teamId = fastChat.teamId
	msgObj.count = fastChat.count

	task = fastChat.task
	if task:
		msgObj.task = task

	target = fastChat.target
	if target:
		msgObj.target.extend(target)
	return msgObj

def broadcastAll(rpcName, msgObj):
	packetData = endPoint.makePacket(rpcName, msgObj)
	for targetSender in chatService.getAllRoleSenderList():
		ep = targetSender.endPoint
		if not ep: # 链接断开时，ep判断为False
			continue
		ep.send(packetData)

def rpcBroadcastAnswerQuick(ep, ctrlr, reqMsg):
	packetData = reqMsg.sValue
	for targetSender in chatService.getAllRoleSenderList():
		ep = targetSender.endPoint
		if not ep: # 链接断开时，ep判断为False
			continue
		if targetSender.level < 15:
			continue
		ep.send(packetData)

def rpcShareAchv(ep, ctrlr, reqMsg):
	'''分享成就
	'''
	msg = {}
	for obj, val in reqMsg.ListFields():
		msg[obj.name] = val

	channelId = msg["channelId"]
	senderId = msg["senderId"]
	content = msg["content"]
	senderObj = chatService.getSender(senderId)
	if senderObj:
		if not chatService.service4terminal.doChannelCost(senderObj, channelId, content):
			return False
		chatService.service4terminal.doChannel(senderObj, channelId, msg)
	else:
		return False
	return True

def rpcUpdateBlack(ep, ctrlr, reqMsg):
	'''更新黑名单
	'''
	roleId = reqMsg.roleId
	targetId = reqMsg.targetId
	isBlack = reqMsg.isBlack

	senderObj = chatService.getSender(roleId)
	if not senderObj:
		return

	if isBlack:
		if targetId not in senderObj.blackList:
			senderObj.blackList[targetId] = 1
	else:
		if targetId in senderObj.blackList:
			senderObj.blackList.pop(targetId)

import chatService
import chatService.service4terminal
import terminal_chat_pb2
import teamTargetData