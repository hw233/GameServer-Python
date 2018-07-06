# -*- coding: utf-8 -*-

def newMonster(*dataList):
	data = {}
	for d in dataList:
		data.update(d)

	monsterObj = Monster()
	monsterObj.name = data["名称"]
	monsterObj.shape = data["造型"]
	if data.get("造型部位"):
		monsterObj.shapeParts = data["造型部位"]
	if data.get("染色"):
		monsterObj.colors = data["染色"]
	monsterObj.level = data["等级"]
	
	monsterObj.hpBase = data["生命"]
	monsterObj.mpBase = data["真气"]
	
	monsterObj.phyDamBase = data["物理伤害"]
	monsterObj.magDamBase = data["法术伤害"]
	monsterObj.phyDefBase = data["物理防御"]
	monsterObj.magDefBase = data["法术防御"]
	
	monsterObj.speBase = data["速度"]
	if data.get("治疗强度"):
		monsterObj.cureBase = data["治疗强度"]
	if data.get("物理抗性"):
		monsterObj.phyRestBase = data["物理抗性"]
	if data.get("法术抗性"):
		monsterObj.magRestBase = data["法术抗性"]
	if data.get("封印命中"):
		monsterObj.sealHitBase = data["封印命中"]
	if data.get("抵抗封印"):
		monsterObj.reSealHitBase = data["抵抗封印"]
	
	if data.get("物理暴击"):
		monsterObj.phyCritBase = data["物理暴击"]
	if data.get("物理抗暴"):
		monsterObj.phyReCritBase = data["物理抗暴"]
	if data.get("法术暴击"):
		monsterObj.magCritBase = data["法术暴击"]
	if data.get("法术抗暴"):
		monsterObj.magReCritBase = data["法术抗暴"]
		
	if data.get("五行"):
		monsterObj.fiveElAttack = data["五行"]
		monsterObj.fiveElDefend = data["五行"]

	if data.get("技能"):
		for skillId in data["技能"]:
			monsterObj.setSkill(skillId, 1)
			
	if data.get("攻击修炼"):
		monsterObj.setSkill(6101, data["攻击修炼"])
	if data.get("物防修炼"):
		monsterObj.setSkill(6102, data["物防修炼"])
	if data.get("法防修炼"):
		monsterObj.setSkill(6103, data["法防修炼"])
	
	if data.get("精通技能"):
		monsterObj.masterPerformList = data["精通技能"]
		
	if data.get("AI集"):
		monsterObj.aiSetList = data["AI集"]

	monsterObj.setup()
	return monsterObj

class Monster(object):
	'''怪物
	'''
	
	def __init__(self):
		self.name = "未知怪物"
		self.shape = 4502 # 造型
		self.shapeParts = [0, 1, 0, 0, 0, 0] # 造型部位
		self.colors = [0, 0, 0, 0, 0, 0] # 染色
		self.level = 1

		self.hp = self.hpBase = self.hpMax = 99 # 生命/生命上限
		self.mp = self.mpBase = self.mpMax = 99 # 真气/真气上限
		
		self.con = 10 # 体质
		self.mag = 10 # 魔力
		self.str = 10 # 力量
		self.res = 10 # 耐力
		self.dex = 10 # 敏捷

		self.phyDam = self.phyDamBase = 99  # 物理伤害
		self.magDam = self.magDamBase = 99  # 法术伤害
		self.phyDef = self.phyDefBase = 99  # 物理防御
		self.magDef = self.magDefBase = 99  # 法术防御
		self.spe = self.speBase = 99  # 速度
		self.cure = self.cureBase = 99 # 治疗强度
		
		self.phyCrit = self.phyCritBase = 0 # 物理暴击
		self.magCrit = self.magCritBase = 0 # 法术暴击
		self.phyReCrit = self.phyReCritBase = 0 # 物理抗暴
		self.magReCrit = self.magReCritBase = 0 # 法术抗暴
		
		self.phyRest = self.phyRestBase = 0 # 物理抗性
		self.magRest = self.magRestBase = 0 # 法术抗性
		
		self.sealHit = self.sealHitBase = 0 # 封印命中
		self.reSealHit = self.reSealHitBase = 0 # 抵抗封印
		
		self.fiveElAttack = FIVE_EL_NONE # 攻击五行
		self.fiveElDefend = FIVE_EL_NONE # 防御五行
		
		self.skillList = {} # 技能列表
		self.performList = [] # 扩展法术
		
		self.applyMgr = container.ApplyMgr()  # 附加效果
		self.lineupObj = None

	def getSkillList(self):
		'''技能列表
		'''
		return self.skillList
	
	def setSkill(self, skillId, level):
		if level == 0: #　删除技能
			self.skillList.pop(skillId)
			return

		skillObj = skill.new(skillId)
		if not skillObj:
			return
		skillObj.level = level
		self.skillList[skillId] = skillObj
	
	def getPerformList(self):
		'''法术列表
		'''
		performList = []
		for skillObj in self.skillList.itervalues():
			performList.extend(skillObj.getPerformList(self))
		
		performList.extend(self.performList)
		return performList
	
	def queryApply(self, name):
		return self.applyMgr.query(name)
	
	def addApply(self, name, val, flag="flag"):
		self.applyMgr.add(name, val, flag)

	def setApply(self, name, val, flag="flag"):
		self.applyMgr.set(name, val, flag)
		
	def removeApply(self, name, flag="flag"):
		self.applyMgr.remove(name, flag)

	def removeApplyByFlag(self, flag):
		self.applyMgr.removeByFlag(flag)
	
	def setup(self):
		'''计算属性
		'''
		self.calSkillApply()
		
		self.hpMax = self.__calAttr("hpMax", self.hpBase, 1000)
# 		self.mpMax = self.__calAttr("mpMax", self.mpBase, 1000)
		
		self.phyDam = self.__calAttr("phyDam", self.phyDamBase)
		self.magDam = self.__calAttr("magDam", self.magDamBase)
		self.phyDef = self.__calAttr("phyDef", self.phyDefBase)
		self.magDef = self.__calAttr("magDef", self.magDefBase)
		
		self.spe = self.__calAttr("spe", self.speBase)
		self.cure = self.__calAttr("cure", self.cureBase)
		
		self.phyCrit = self.__calAttr("phyCrit", self.phyCritBase)
		self.magCrit = self.__calAttr("magCrit", self.magCritBase)
		self.phyReCrit = self.__calAttr("phyReCrit", self.phyReCritBase)
		self.magReCrit = self.__calAttr("magReCrit", self.magReCritBase)
		
		self.sealHit = self.__calAttr("sealHit", self.sealHitBase)
		self.reSealHit = self.__calAttr("reSealHit", self.reSealHitBase)
				
		self.hp = self.hpMax
		self.mp = self.mpMax
		
	def calSkillApply(self):
		'''计算技能效果
		'''
		self.applyMgr.removeByPrefix("sk")
		for skillObj in self.getSkillList().itervalues():
			skillObj.setup(self)

	def __calAttr(self, attr, val=0, ratio=100):
		val = val + self.queryApply(attr)
		val = val * (ratio + self.queryApply("%sRatio" % attr)) / ratio
		return max(0, int(val))
	
	def getColors(self):
		'''染色
		'''
		return self.colors
	
	def getLineupObj(self):
		'''获取阵法对象 
		'''
		return self.lineupObj
	
	def setLineupObj(self, lineupObj):
		'''设置阵法对象
		'''
		self.lineupObj = lineupObj


from perform.defines import *
import container
import skill
import war.ai