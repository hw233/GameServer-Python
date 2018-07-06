# -*- coding: utf-8 -*-
import pst

class Lineup(pst.cEasyPersist):
	'''阵法
	'''
	
	def __init__(self, lineupId):
		pst.cEasyPersist.__init__(self)
		self.id = lineupId
		self.ownerId = 0
		
	def load(self, data):
		if not data:
			return
		pst.cEasyPersist.load(self, data.get("data"))
			
	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		return data
	
	def getConfig(self, key):
		'''读取导表数据
		'''
		data = lineupData.getLineupData(self.id)
		return data[key]
		
	@property
	def key(self):
		return self.id
	
	@property
	def name(self):
		return self.getConfig("名称")

	@property
	def level(self):
		return self.fetch("level", 1)
	
	@level.setter
	def level(self, level):
		if level > self.getLevelMax():
			return
		self.set("level", level)
	
	def getLevelMax(self):
		'''最高等级
		'''
		return 5
	
	def getExp(self):
		return self.fetch("exp")
	
	def setExp(self, val):
		self.set("exp", val)
		
	def getExpNext(self):
		'''下级经验
		'''
		return lineupData.getExpNext(self.level+1)
	
	def setup(self, who):
		pass
	
	def cancelSetup(self, who):
		pass
	
	def setupWarrior(self, w):
		'''战斗中效果
		'''
		effectList = lineupData.getEffectList(self.id, w.pos)
		for effectName, effectVal in effectList.iteritems():
			effectRatio = lineupData.getEffectRatio(self.level)
			effectVal = int(effectVal * effectRatio)
			w.addApply(effectName, effectVal, "lineup")

	def getEyeId(self):
		'''获取阵眼id
		'''
		return self.fetch("eyeId")

	def getEyeObj(self):
		'''获取阵眼对象
		'''
		if hasattr(self, "eyeObj"):
			return self.eyeObj

		eyeId = self.getEyeId()
		if not eyeId:
			return None

		who = getRole(self.ownerId)
		if who:
			return who.eyeCtn.getItem(eyeId)
		return None
	
	def setEyeObj(self, eyeObj):
		'''设置阵眼对象
		'''
		oldEyeObj = self.getEyeObj()
		if eyeObj != oldEyeObj:  #穿上
			if oldEyeObj:
				oldEyeObj.setLineupId(0)
			self.set("eyeId", eyeObj.id)
			eyeObj.setLineupId(self.id)
		else:
			self.delete("eyeId")
			eyeObj.setLineupId(0)
		
		who = getRole(self.ownerId)
		if who:
			lineup.service.rpcLineupMod(who, self, "eyeId")


class Eye(pst.cEasyPersist):
	'''阵眼
	'''
	
	def __init__(self, eyeId=0):
		pst.cEasyPersist.__init__(self)
		self.id = eyeId
		self.ownerId = 0
		
		self.hp = self.hpMax = 99  # 生命/生命上限
		self.mp = self.mpMax = 99  # 真气/真气上限
		
		self.phyDam = 0  # 物理伤害
		self.magDam = 0  # 法术伤害
		self.phyDef = 0  # 物理防御
		self.magDef = 0  # 法术防御
		self.cure = 0 #治疗
		
		self.phyCrit = 3 # 物理暴击
		self.magCrit = 3 # 法术暴击
		self.phyReCrit = 0 # 物理抗暴
		self.magReCrit = 0 # 法术抗暴
		
		self.applyMgr = container.ApplyMgr()  # 附加效果
		
	def load(self, data):
		if not data:
			return
		pst.cEasyPersist.load(self, data["data"])
		
	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		return data

	def no(self):
		'''物品编号
		'''
		return self.getConfig("物品")

	@property
	def key(self):
		return self.id
	
	def setNo(self, eyeNo):
		'''设置导表编号
		'''
		self.set("no", eyeNo)
	
	def getNo(self):
		'''导表编号
		'''
		return self.fetch("no")
	
	def getConfig(self, key):
		'''读取导表数据
		'''
		data = lineupData.getLineupEyeData(self.getNo())
		return data[key]
	
	@property
	def name(self):
		return self.getConfig("名称")
	
	@property
	def level(self):
		'''等级
		'''
		if hasattr(self, "_level"):
			return self._level

		who = getRole(self.ownerId)
		if who:
			return who.level
		return 0
	
	@level.setter
	def level(self, level):
		'''设置等级
		'''
		self._level = level
	
	def _initData(self):
		shapeStr = self.getConfig("造型")
		shape, shapeParts = template.transShapeStr(shapeStr)
		self._shape = shape
		self._shapeParts = shapeParts
	
	@property
	def shape(self):
		'''造型
		'''
		if not hasattr(self, "_shape"):
			self._initData()
		return self._shape
	
	@property
	def shapeParts(self):
		'''造型部位
		'''
		if not hasattr(self, "_shapeParts"):
			self._initData()
		return self._shapeParts
	
	@property
	def spe(self):
		'''速度
		'''
		data = monsterBase.getBaseAbleInfo(self.level)
		speBase = data["速度"]
		return int(speBase * self.getSpeRatio() / 100)
	
	def getSpeRatio(self):
		'''速度系数
		'''
		return self.fetch("speRatio")

	def setSpeRatio(self, speRatio):
		'''设置速度系数
		'''
		return self.set("speRatio",speRatio)
	
	def setStar(self, isStar):
		'''设置是否变星
		'''
		if isStar:
			self.set("star", 1)
		else:
			self.delete("star")
	
	def isStar(self):
		'''是否变星
		'''
		if self.fetch("star"):
			return True
		return False

	def setLineupId(self, lineupId):
		'''设置阵法id
		'''
		if lineupId:
			self.set("lineupId", lineupId)
		else:
			self.delete("lineupId")

		who = getRole(self.ownerId)
		if who:
			lineup.service.rpcEyeMod(who, self, "isUse")

	def getLineupId(self):
		'''获取阵法id
		'''
		return self.fetch("lineupId")
	
	def isUse(self):
		'''是否装备中
		'''
		if self.getLineupId():
			return True
		return False

	def skillCount(self):
		'''技能数量
		'''
		return len(self.skillList)
	
	def setSkill(self, skillId, level=1):
		'''设置技能
		'''
		skillList = self.fetch("skillList", [])
		if level > 0: # 增加
			if skillId not in skillList: 
				skillList.append(skillId)
		else: # 删除
			if skillId in skillList:
				skillList.remove(skillId)

		self.set("skillList", skillList)
		self.generateSkillList()

	def querySkillLevel(self, skillId):
		'''查询技能等级
		'''
		if skillId in self.getSkillList():
			return 1
		return 0

	def getSkillList(self):
		'''技能列表
		'''
		if not hasattr(self, "skillList"):
			self.generateSkillList()
		return self.skillList

	def getSkillListByOrder(self):
		'''有顺序的技能列表
		'''
		if not hasattr(self, "skillList"):
			self.generateSkillList()
		
		skillList = []
		for skillId in  self.fetch("skillList", []):
			skillObj = self.skillList[skillId]
			skillList.append((skillId, skillObj))
			
		return skillList
	
	def generateSkillList(self):
		'''生成技能列表，临时的
		'''
		self.skillList = {}
		for skillId in self.fetch("skillList", []):
			skillObj = skill.new(skillId)
			if not skillObj:
				continue
			skillObj.level = 1
			self.skillList[skillId] = skillObj
	
	def getPerformList(self):
		'''法术列表
		'''
		performList = []
		skillList = self.getSkillList()
		for skillId, skillObj in skillList.iteritems():
			if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略该低级技能
				continue
			performList.extend(skillObj.getPerformList(self))
		
		return performList
		
	def getStallCD(self):#摆摊cd
		dayNo = self.fetch("stall")
		if not dayNo:
			return 0

		day = dayNo - getDayNo()
		if day <= 0:
			self.delete("stall")
			return 0

		return day


# 	def queryApply(self, name):
# 		return self.applyMgr.query(name)
# 	
# 	def addApply(self, name, val, flag="flag"):
# 		self.applyMgr.add(name, val, flag)
	
# 	def reCalcAttr(self):
# 		'''计算属性
# 		'''
# 		self.applyMgr.removeByPrefix("sk")
# 		for skillObj in self.getSkillList().itervalues():
# 			skillObj.setup(self)
		
# 		self.hpMax = self.__calAttr("hpMax", self.hpBase, 1000)
# 		self.mpMax = self.__calAttr("mpMax", self.mpBase, 1000)
# 		
# 		self.phyDam = self.__calAttr("phyDam", self.phyDamBase)
# 		self.magDam = self.__calAttr("magDam", self.magDamBase)
# 		self.phyDef = self.__calAttr("phyDef", self.phyDefBase)
# 		self.magDef = self.__calAttr("magDef", self.magDefBase)
# 		
# 		self.spe = self.__calAttr("spe", self.speBase)
# 		self.cure = self.__calAttr("cure", self.cureBase)
# 		
# 		self.phyCrit = self.__calAttr("phyCrit", self.phyCritBase)
# 		self.magCrit = self.__calAttr("magCrit", self.magCritBase)
# 		self.phyReCrit = self.__calAttr("phyReCrit", self.phyReCritBase)
# 		self.magReCrit = self.__calAttr("magReCrit", self.magReCritBase)
# 				
# 		self.hp = self.hpMax
# 		self.mp = self.mpMax

# 	def __calAttr(self, attr, valBase=0, ratio=100):
# 		val = valBase + self.queryApply(attr)
# 		val = val * (ratio + self.queryApply("%sRatio" % attr)) / ratio
# 		return max(1, int(val))
		

from common import *
import lineupData
import lineup
import skill
import monsterBase
import lineup.service
import template
import container