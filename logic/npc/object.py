# -*- coding: utf-8 -*-
import entity

class NpcBase(entity.cEntity):
	'''npc基类
	'''
	idx = 0  # 固定npc的导表编号，用于任务等
	shape = 4502 # 造型
	shapeParts = [0, 1, 0, 0, 0, 0] # 造型部位
	colors = [0, 0, 0, 0, 0, 0] # 染色
	action = 0 # 动作
	effectId = 0 # 特效编号

	def __init__(self):
		entity.cEntity.__init__(self)
		npc.gNPCproxy.addObj(self, self.id)
		self.sSerialized1 = None
	
	def ettType(self):  # override
		return entity.ETT_TYPE_NPC
	
	def trigger(self, ep, who):  # 被触碰了
		who.lastNpcId = self.id
		self.triggerNpc = self.id # 被触碰的npc
		self.doLook(who)
		if hasattr(self, "triggerNpc"):
			del self.triggerNpc
		
	def doLook(self, who):
		pass

	def say(self, who, content):
		'''npc对话框
		'''
		if hasattr(self, "triggerNpc"):
			npcId = self.id
			del self.triggerNpc
		else:
			npcId = 0

		import message
		message.npcSayByArgs(who, content, self.name, self.shape, npcId)

	def getSerialized1(self):  # 场景广播包
		if self.sSerialized1 is None:
			npcInfo = scene_pb2.npcInfo()
			# npcInfo.iEttId=self.id
			npcInfo.iShape = self.shape
			npcInfo.sName = self.name
			npcInfo.shapeParts.extend(self.shapeParts)
			npcInfo.colors.extend(self.colors)
			npcInfo.iNo = self.idx
			npcInfo.title = self.title
			npcInfo.effectId = self.effectId
			npcInfo.d = self.d
			npcInfo.action = self.action
			npcInfo.addon = self.getAddon()
			# npcInfo.iDialog=self.dialog()
			# npcInfo.fScaleX=self.scaleX()
			# npcInfo.fScaleY=self.scaleY()
			# npcInfo.voices.extend([str(v) for v in self.voices()])	#序列化声音
				
			ettEnter = scene_pb2.entityEnter()
			ettEnter.iEttId = self.id
			ettEnter.iEttType = self.ettType()
			ettEnter.iX = self.x
			ettEnter.iY = self.y
			ettEnter.iSceneId = self.getHolderScene().id
			ettEnter.sSerializedEtt = npcInfo.SerializeToString()
			self.sSerialized1 = endPoint.makePacket('rpcEttEnter', ettEnter)
		return self.sSerialized1

	# def getSerializedGroup(self):  # override 场景广播包组
	# 	return [self.getSerialized1(), ]
	
	def getColors(self):
		return self.colors
	
	def getChat(self):
		'''对白
		'''
		if hasattr(self, "chatList"):
			chatIdx = self.chatList[rand(len(self.chatList))]
			return "$D%d" % chatIdx
		return ""

	def getEttBaseSerialized(self):#override
		if not self.sEnterSerialized:
			npcInfo = scene_pb2.npcInfo()
			npcInfo.iShape = self.shape
			npcInfo.sName = self.name
			npcInfo.shapeParts.extend(self.shapeParts)
			npcInfo.colors.extend(self.colors)
			npcInfo.iNo = self.idx
			npcInfo.title = self.title
			npcInfo.effectId = self.effectId
			npcInfo.d = self.d
			npcInfo.action = self.action
			npcInfo.addon = self.getAddon()
			self.sEnterSerialized  = npcInfo.SerializeToString()
		return self.sEnterSerialized
	
	def getAddon(self):
		'''附加状态
		'''
		return 0
	
	def attrChange(self, *attrNameList):
		'''修改属性
		'''
		attrList = {}
		for attrName in attrNameList:
			attrVal = getValByName(self, attrName)
			attrList[attrName] = attrVal
		
		import scene
		scene.broadcastEttChange(self, attrList)


class cNpc(NpcBase):
	'''固定npc
	'''

	def __init__(self):
		NpcBase.__init__(self)
		
# 	def trigger(self, ep, who):
# 		who.lastNpcId = self.id
# 		
# 		# 暂时不删除
# 		taskList = []
# 		for taskObj in who.taskCtn.getAllValues():
# 			if self.idx in taskObj.eventList:
# 				taskList.append(taskObj)
# 				
# 		teamObj = who.getTeamObj()
# 		if teamObj and teamObj.isLeader(who.id):
# 			for taskObj in teamObj.taskCtn.getAllValues():
# 				if self.idx in taskObj.eventList:
# 					taskList.append(taskObj)
# 				
# 		if len(taskList) == 1:
# 			taskList[0].quest(who, self)
# 		else:
# 			self.doLook(who)
		
	def doLook(self, who):
		chat = self.getChat()
		if chat:
			self.say(who, chat)

# 	@property
# 	def name(self):
# 		if hasattr(self, "_name"):
# 			return self._name
# 		return self.getConfig('名字', '')
# 	
# 	@name.setter
# 	def name(self, name):
# 		self._name = name

	# def menuName(self):
	# 	 return None

# 	@property
# 	def shape(self):  # override
# 		if hasattr(self, "_shape"):
# 			return self._shape
# 		return self.getConfig('造型', 0)
# 	
# 	@shape.setter
# 	def shape(self, shape):
# 		self._shape = shape

	# def dialog(self):#override
	# 	 return self.getConfig('dialog',0)

	# def scaleX(self):
	# 	 return self.getConfig('scaleX',0)

	# def scaleY(self):
	# 	 return self.getConfig('scaleY',0)

	def voices(self):
		return self.getConfig('voices', [])
		
	def getConfig(self, sKey, uDefault=0):
		return npcData.getConfig(self.idx, sKey, uDefault)
	
	def getChat(self):
		chatList = self.getConfig("对白编号")
		if chatList:
			chatIdx = chatList[rand(len(chatList))]
			return "$D%d" % chatIdx
		return ""

	@property
	def kind(self):
		return self.getConfig("类型")

from common import *
import npc
import scene_pb2
import npcData
import u
import endPoint
import message
