# -*- coding: utf-8 -*-
import pst

class Skill(pst.cEasyPersist):
	'''技能基类
	'''
	id = 0 # 技能id
	name = ""
	score = 0 # 评分
	performList = () # 对应法术
	applyList = {} # 技能效果

	def __init__(self):
		pst.cEasyPersist.__init__(self)
		self.ownerId = 0
		
	@property
	def key(self):
		return self.id
	
	def getConfig(self, key):
		raise NotImplementedError,"请在子类实现"

	@property
	def level(self):
		return self.fetch("level", 0)
	
	@level.setter
	def level(self, level):
		self.set("level", level)
	
	def getLevelMax(self, obj=None):
		if hasattr(self, "levelMax"):
			return self.levelMax
		if obj:
			return obj.level
		return 1
	
	def setup(self, obj):
		'''设置
		'''
		for name, val in self.applyList.iteritems():
			val = int(self.transCode(val, obj))
			self.addApply(obj, name, val)
		self.onSetup(obj)
		
	def onSetup(self, obj):
		pass
	
	def cancelSetup(self, obj):
		obj.removeApplyByFlag("sk%d" % self.id)
		self.onCancelSetup(obj)
		
	def onCancelSetup(self, obj):
		pass
	
	def addApply(self, obj, name, val):
		obj.addApply(name, val, "sk%d" % self.id)
		
	def removeApply(self, obj, name):
		obj.removeApply(name, "sk%d" % self.id)
	
	def getPerformList(self, obj):
		'''法术列表
		'''
		if hasattr(self, "performList"):
			return self.performList
		return []
	
	def transCode(self, code, obj=None):
		import common
		return common.transCode(self, code, obj)
	
	def getValueByVarName(self, varName, obj=None):
		if varName == "LV":
			return obj.level
		if varName == "SLV":
			return self.level
		if varName == "RND":
			return rand
		raise Exception("策划填的变量{}无法解析".format(varName))


class NpcSkill(Skill):
	'''npc技能
	'''
	pass




class SchSkill(Skill):
	'''职业技能
	'''
	
	def getConfig(self, key):
		import skillSchData
		return skillSchData.getConfig(self.id, key)
	
	def getOpenLevel(self):
		return self.getConfig("开启等级")
	
	@property
	def school(self):
		return self.getConfig("职业")



class GuildSkill(Skill):
	'''帮派技能
	'''
	
	def getConfig(self, key):
		import skillGuildData
		return skillGuildData.getConfig(self.id, key)
		
	def getEffectVal(self, who=None):
		return self.transCode(self.getConfig("效果值"), who)
	
	def getLevelMax(self, obj=None):
		return obj.level + 10

	
class EquipSkill(Skill):
	'''装备技能(特技特效)
	'''
	pass


class PracticeSkill(Skill):
	'''修炼技能
	'''
	
	def getLevelMax(self, obj=None):
		return 25
	
	def getPointNext(self):
		'''下级所需修炼点
		'''
		import skillPraticeLevelData
		return skillPraticeLevelData.getPointNext(self.name, self.level + 1)
	
	def setPoint(self, val):
		'''设置修炼点
		'''
		self.set("point", val)
		
	def getPoint(self):
		'''获取修炼点
		'''
		return self.fetch("point", 0)

	
from common import *
