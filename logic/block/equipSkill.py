# -*- coding: utf-8 -*-

class cContainer(object):
	'''装备技能容器
	'''
	
	def __init__(self, ownerId):
		self.ownerId = ownerId
		self.skillList = {} # 每个装备的技能列表
		self.countList = {} # 每个技能的数量
		
	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)
	
	def getOwnerObj(self):
		return getRole(self.ownerId)

	def addItem(self, propsId, skillObj):
		skId = skillObj.id
		if propsId not in self.skillList:
			self.skillList[propsId] = {}
		self.skillList[propsId][skId] = skillObj
		if skId in self.countList:
			self.countList[skId] += 1
		else:
			self.countList[skId] = 1
			self.setup(skillObj)
			self._rpcAddItem(skillObj)
	
	def getItem(self, skId):
		for skillList in self.skillList.itervalues():
			if skId in skillList:
				return skillList[skId]
		return None
	
	def removeItemByPropsId(self, propsId):
		skillList = self.skillList.pop(propsId, None)
		if not skillList:
			return
		for skId, skillObj in skillList.items():
			count = self.countList.get(skId, 0) - 1
			if count > 0:
				self.countList[skId] = count
			else:
				del self.countList[skId]
				self.cancelSetup(skillObj)
				self._rpcRemoveItem(skillObj)
				
	def setup(self, obj):
		who = self.getOwnerObj()
		if who and hasattr(obj, "setup"):
			obj.setup(who)
		
	def cancelSetup(self, obj):
		who = self.getOwnerObj()
		if who and hasattr(obj, "cancelSetup"):
			obj.cancelSetup(who)
				
	def getLevel(self, skId):
		skillObj = self.getItem(skId)
		if skillObj:
			return skillObj.level
		return 0

	def getAllValues(self):
		lst = {}
		for skillList in self.skillList.itervalues():
			lst.update(skillList)
		return lst.values()
	
	def _rpcAddItem(self, skillObj):
		who = self.getOwnerObj()
		skill.service.rpcSkillAdd(who, skillObj)

	def _rpcRemoveItem(self, skillObj):
		who = self.getOwnerObj()
		skill.service.rpcSkillDelete(who, skillObj.id)


from common import *
import skill.service