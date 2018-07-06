# -*- coding: utf-8 -*-
import ctn
import block

# 玩家的技能容器
class cSkillContainer(ctn.LevelContainer, block.cCtnBlock):

	def __init__(self, iOwnerId):
		block.cCtnBlock.__init__(self, '技能数据块', iOwnerId)
		ctn.cContainerBase.__init__(self, iOwnerId)

		self.setIsStm(sql.SKILL_INSERT)
		self.setDlStm(sql.SKILL_DELETE)
		self.setUdStm(sql.SKILL_UPDATE)
		self.setSlStm(sql.SKILL_SELECT)

	def _createAndLoadItem(self, iIndex, uData):  # override
		iNo, dData = uData
		return skill.createAndLoad(iNo, dData)
	
	def _newItem(self, key):
		return skill.new(key)
		
	def setItemLevel(self, skillObj, level):
		ctn.LevelContainer.setItemLevel(self, skillObj, level)
		self.cancelSetup(skillObj)
		self.setup(skillObj)
	
	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)
	
	def setup(self, skillObj, isLogin=False):
		who = self.getOwnerObj()
		if who and hasattr(skillObj, "setup"):
			skillObj.setup(who)
		
	def cancelSetup(self, skillObj):
		who = self.getOwnerObj()
		if who and hasattr(skillObj, "cancelSetup"):
			skillObj.cancelSetup(who)

	def _rpcAddItem(self, skillObj):
		who = self.getOwnerObj()
		skill.service.rpcSkillAdd(who, skillObj)

	def _rpcRemoveItem(self, skillObj):  # override
		who = self.getOwnerObj()
		skill.service.rpcSkillDelete(who, skillObj.id)
		
	def _rpcSetLevel(self, skillObj):
		who = self.getOwnerObj()
		skill.service.rpcSkillChange(who, skillObj, "level")

	def _rpcRefresh(self):
		who = self.getOwnerObj()
		skill.service.rpcSkillLevelAll(who)

	def _dirtyEventHandler(self):  # override
		factoryConcrete.skillFtr.schedule2tail4save(self.ownerId)
		
	def addPracticePoint(self, skillId, point):
		'''增加修炼技能的修炼点
		'''
		skillObj = self.getItem(skillId)
		if not skillObj:
			skillObj = self._newItem(skillId)
			skillObj.level = 0
			self.addItem(skillObj)
		
		levelMax = skillObj.getLevelMax()
		if skillObj.level >= levelMax:
			return

		point = skillObj.getPoint() + point
		while point >= skillObj.getPointNext():
			point = point - skillObj.getPointNext()
			skillObj.level += 1
			if skillObj.level >= levelMax:
				break
			
		skillObj.setPoint(point)
		
		who = self.getOwnerObj()
		skill.service.rpcSkillChange(who, skillObj, "level", "point")


from common import *
import sql
import factoryConcrete
import skill
import u
import container
import skill.service
