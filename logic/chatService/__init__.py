# -*- coding: utf-8 -*-
'''聊天系统
'''

def init():
	global gEndPointKeeper, gRoleIdMapEndPoint, gSenderMgr, gChannelMgr, gAudioMgr
	gEndPointKeeper = misc.cEndPointKeeper()  # endPoint id 映射 endPoint
	gRoleIdMapEndPoint = chatService.object.EndPointProxyManager()  # 角色id映射endPoint,value是proxy
	gSenderMgr = {}  # 发送者id映射sender
	gChannelMgr = chatService.object.ChannelMgr() # 频道管理器
	gAudioMgr = chatService.object.cAudioMgr() # 语音信息管理器
	newSender(SYS_SENDER_ID) # 创建系统发送者

def getSender(senderId):
	'''获取发送者
	'''
	return gSenderMgr.get(senderId)

def getSysSender():
	'''获取系统发送者
	'''
	return getSender(SYS_SENDER_ID)
	
def getAllRoleSenderList():
	'''获取全部角色发送者
	'''
	for senderObj in gSenderMgr.itervalues():
		if senderObj.id == SYS_SENDER_ID:
			continue
		yield senderObj
	
def newSender(senderId, data=None):
	'''新建发送者
	'''
	if senderId == SYS_SENDER_ID: # 系统发送者
		senderObj = chatService.object.SysSender(SYS_SENDER_ID)
	else: # 角色发送者
		senderObj = chatService.object.RoleSender(senderId)
	
	senderObj.init(data)
	addToSenderMgr(senderObj.id, senderObj)
	return senderObj

def addToSenderMgr(senderId, senderObj):
	'''加入发送者管理器
	'''
	gSenderMgr[senderObj.id] = senderObj

def removeFromSenderMgr(senderId):
	'''从发送者管理器中移除
	'''
	if senderId in gSenderMgr:
		del gSenderMgr[senderId]

def removeAudio(iAudioIdx):
	'''移除语音信息
	'''
	oCenterEp = client4center.getCenterEp4ss()
	if oCenterEp:
		oCenterEp.rpcDelAudio(iAudioIdx)

def getMainEP():
	'''主服务器
	'''
	return backEnd.gMainEp4cs

from chatService.defines import *
import misc
import u
import chatService.object
import backEnd
import client4center
