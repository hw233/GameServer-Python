# -*- coding: utf-8 -*-
from chatService.defines import *
import misc

class EndPointProxyManager(misc.cEndPointProxyManager):
	'''endPoint管理器
	'''

	def _getEndPoint(self, epId):
		return chatService.gEndPointKeeper.getObj(epId)



#===============================================================================
# 消息发送者相关
#===============================================================================
class Sender(object):
	'''消息发送者
	'''
	def __init__(self, senderId):
		self.id = senderId
		
	def init(self, data):
		'''出生
		'''
		pass
	
	def update(self, data):
		'''更新
		'''
		
	def getMsg(self):
		raise NotImplementedError("请在子类实现")


class SysSender(Sender):
	'''系统发送者
	'''
	def getMsg(self):
		msgObj = terminal_chat_pb2.senderInfo()
		msgObj.senderId = self.id
		return msgObj


class RoleSender(Sender):
	'''角色发送者
	'''
	
	def __init__(self, senderId):
		Sender.__init__(self, senderId)
		self.shape = 0
		self.name = ""
		self.level = 0
		self.flagList = []
		self.guildName = ""
		
		self.sceneId = 0
		self.schoolId = 0
		self.teamId = 0
		self.guildId = 0
		self.warId = 0
		self.guildBan = 0
		
		self.channelBanList = [] #频道屏蔽列表
		self.blackList = {} # 黑名单
	
	def init(self, data):
		self.update(data)
		
	def update(self, data):
		for attrName, attrVal in data.iteritems():
			if attrName == "blackList":
				self.updateBlackList(attrVal)
				continue
			attrValOld = getattr(self, attrName, 0)
			setattr(self, attrName, attrVal)
			self.updateChannel(attrName, attrValOld, attrVal)

	def updateBlackList(self, blackList):
		'''更新黑名单
		'''
		for blackId in blackList:
			self.blackList[blackId] = 1
			
	def updateChannel(self, attrName, attrValOld, attrValNew):
		'''更新频道
		'''
		if attrValOld == attrValNew:
			return
		channelId = attrName2ChannelId.get(attrName)
		if not channelId:
			return

		if attrValOld:
			chatService.gChannelMgr.leaveChannel(self.id, channelId, attrValOld)
		if attrValNew:
			chatService.gChannelMgr.enterChannel(self.id, channelId, attrValNew)
			
	def leaveAllChannel(self):
		'''离开所有频道
		'''
		for attrName, channelId in attrName2ChannelId.iteritems():
			attrVal = getattr(self, attrName, 0)
			if attrVal:
				chatService.gChannelMgr.leaveChannel(self.id, channelId, attrVal)
			
	def release(self):
		'''释放
		'''
		chatService.removeFromSenderMgr(self.id)
		self.leaveAllChannel()

	def getMsg(self):
		msgObj = terminal_chat_pb2.senderInfo()
		msgObj.senderId = self.id
		msgObj.shape = self.shape
		msgObj.name = self.name
		msgObj.level = self.level
		msgObj.flagList.extend(self.flagList)
		msgObj.guildName = self.guildName
		msgObj.teamId = self.teamId
		msgObj.school = self.schoolId
		return msgObj
	
	@property
	def endPoint(self):
		return chatService.gRoleIdMapEndPoint.getProxy(self.id)

	def isChannelBaned(self, channelId, senderId=0):
		'''频道是否被屏蔽
		'''
		if senderId:
			if senderId in self.blackList: # 黑名单的要屏蔽
				return 1
			if senderId == self.id: #  对自己不屏蔽
				return 0
		if channelId == CHANNEL_SYS_ANNOUNCE: # 系统公告不可屏蔽
			return 0
		if channelId == CHANNEL_SYS_MESSAGE: # 屏蔽系统频道也对传闻生效
			channelId = CHANNEL_SYS_ANNOUNCE
		elif channelId == CHANNEL_FIGHT: # 屏蔽当前频道也对战斗频道生效
			channelId = CHANNEL_CURRENT
		return channelId in self.channelBanList

#===============================================================================
# 频道管理相关
#===============================================================================
class ChannelMgr(object):
	'''频道管理器
	'''
	def __init__(self):
		self.channelList = { # 频道列表
			CHANNEL_SCHOOL: {},
			CHANNEL_TEAM: {},
			CHANNEL_GUILD: {},
			CHANNEL_FIGHT: {},
		}
		
		self.channelBanList = {}  # 频道屏蔽列表
		
	def enterChannel(self, roleId, channelId, targetId):
		'''进入频道
		'''
		channelList = self.channelList[channelId]
		if targetId not in channelList:
			channelList[targetId] = {}
		channelList[targetId][roleId] = 1
		
	def leaveChannel(self, roleId, channelId, targetId):
		'''离开频道
		'''
		channelList = self.channelList[channelId]
		if targetId in channelList:
			if roleId in channelList[targetId]:
				del channelList[targetId][roleId]
					
	def getRoleIdList(self, channelId, targetId):
		'''获取指定频道的角色id
		'''
		roleIdList = self.channelList[channelId].get(targetId, {})
		return roleIdList.keys()


class cAudio(object):
	'''语音
	'''
	def __init__(self, idx, sContent):
		self.audioIdx = idx
		self.audioContent = sContent

	def getMsg(self):
		msg = terminal_chat_pb2.audioInfo()
		msg.audioIdx = self.audioIdx
		msg.audioLen = self.audioLen
		return msg


class cAudioMgr(object):
	'''语音管理
	'''
	def __init__(self):
		# 各频道语音上限
		self.channelMax = {
		CHANNEL_SCHOOL : 1000,
		CHANNEL_TEAM : 1000,
		CHANNEL_GUILD : 1000,
		CHANNEL_WORLD : 1000,
		}
		self.channelList = { # 频道语音列表
			CHANNEL_SCHOOL: [],
			CHANNEL_TEAM: [],
			CHANNEL_GUILD: [],
			CHANNEL_WORLD: [],
		}

	def addAudio(self, iChId, iIdx, iLen):
		'''将语音信息加入管理器
		'''
		chList = self.channelList.get(iChId, [])
		maxAudio = self.channelMax.get(iChId, 1000)
		# 若语音对象过多，删除早期的语音
		if len(chList) >= maxAudio:
			chList.pop(0) # 删除频道最早的语音
			chatService.removeAudio(iIdx) # 将语音对象从keeper中移除
		chList.append(iIdx)
		msg = terminal_chat_pb2.audioInfo()
		msg.audioIdx = iIdx
		msg.audioLen = iLen
		return msg


from chatService.defines import *
import chatService
import terminal_chat_pb2
import keeper
