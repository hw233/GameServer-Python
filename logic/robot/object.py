# -*- coding: utf-8 -*-
import endPointWithSocket

class EndPointWithSocket(endPointWithSocket.cEndPointWithSocket):

	def _onDisConnected(self):
		if self.accountName in robot.gClientList:
			del robot.gClientList[self.accountName]
		if self.roleId in robot.gClientRoleList:
			del robot.gClientRoleList[self.roleId]
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		

class ClientEntity(object):
	'''客户端实体
	'''
	
	def __init__(self, entityId):
		self.id = entityId
		self.name = "未知实体%d" % self.id
		self.shape = 0
		self.sceneId = 0
		self.x = 0
		self.y = 0
		
	def updateAttr(self, data):
		for attrName, attrVal in data.items():
			setattr(self, attrName, attrVal)
	
	

class ClientRole(ClientEntity):
	'''客户端角色
	'''
	
	def __init__(self, accountName, roleId):
		ClientEntity.__init__(self, roleId)
		
		self.accountName = accountName
		self.name = "未知角色%d" % self.id
		self.school = 0
		
		self.timerMgr = timer.cTimerMng() # 定时器
		self.aiList = {} # 正在执行的AI

	@property
	def endPoint(self):
		clientObj = robot.getClient(self.accountName)
		return clientObj.ep
	
	def updateAttr(self, data):
# 		print "updateAttr", "roleId:%s" % self.id, data
		for attrName, attrVal in data.items():
			if attrName == "roleId":
				attrName = "id"
			setattr(self, attrName, attrVal)
			
	def startTimer(self, func, ti, flag, interval=0):
		'''定时器开始
		'''
		self.timerMgr.run(func, ti, interval, flag)
		
	def stopTimer(self, flag):
		'''定时器结束
		'''
		self.timerMgr.cancel(flag)
		
	def hasTimer(self, flag):
		'''是否有定时器
		'''
		return self.timerMgr.hasTimerId(flag)
	
	def removeAI(self, aiName):
		'''移除AI
		'''
		if aiName in self.aiList:
			del self.aiList[aiName]
		
	def addAI(self, aiName):
		'''增加AI
		'''
		self.aiList[aiName] = 1
		
	def hasAI(self, aiName):
		'''是否拥有AI
		'''
		return aiName in self.aiList
	
	def inWar(self):
		'''是否战斗中
		'''
		return getattr(self, "war", None)
	
	
class ClientNpc(ClientEntity):
	'''客户端Npc
	'''
	
	def __init__(self, npcId):
		ClientEntity.__init__(self, npcId)
		self.name = "未知npc%d" % self.id
		self.idx = 0
		
	
import timer
import robot