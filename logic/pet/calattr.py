# -*- coding: utf-8 -*-

def calcAttr(petObj):
	'''计算属性
	'''
	attrData = {}

	_calSkillApply(petObj)
		
	# 基础属性
	attrData["con"] = con = _calAttr(petObj, "con")
	attrData["mag"] = mag = _calAttr(petObj, "mag")
	attrData["str"] = _str = _calAttr(petObj, "str")
	attrData["res"] = res = _calAttr(petObj, "res")
	attrData["spi"] = spi = _calAttr(petObj, "spi")
	attrData["dex"] = dex = _calAttr(petObj, "dex")
	
	# 主属性
	hpGen = petObj.getHpGen()
	phyAttGen = petObj.getPhyAttGen()
	magAttGen = petObj.getMagAttGen()
	phyDefGen = petObj.getPhyDefGen()
	magDefGen = petObj.getMagDefGen()
	speGen = petObj.getSpeGen()
	grow = petObj.getGrow()
	level = petObj.level
	
	attrData["hpMax"] = _calAttr(petObj, "hpMax", (con * hpGen / 1000 + level * 15) * grow + 50, 1000)
	attrData["mpMax"] = _calAttr(petObj, "mpMax", mag * 1 + level * 5 + 200, 1000)
	
	attrData["phyDam"] = _calAttr(petObj, "phyDam", (_str * 1 * phyAttGen / 1000 + level * 5) * grow + 20)
	attrData["magDam"] = _calAttr(petObj, "magDam", (mag * 1 * magAttGen / 1000 + level * 5) * grow + 20)
	attrData["phyDef"] = _calAttr(petObj, "phyDef", (res * 1 * phyDefGen / 1000 + level * 2) * grow + 5)
	attrData["magDef"] = _calAttr(petObj, "magDef", (spi * 1 * magDefGen / 1000 + level * 2) * grow + 5)
	attrData["spe"] = _calAttr(petObj, "spe", (con * 0.2 + mag * 0.2 + _str * 0.2 + res * 0.2 + spi * 0.2 + dex * 1.5 * speGen / 1000 + level * 2) * grow + 5)
	
	attrData["phyCrit"] = _calAttr(petObj, "phyCrit", 3)
	attrData["magCrit"] = _calAttr(petObj, "magCrit", 3)
	attrData["phyReCrit"] = _calAttr(petObj, "phyReCrit", 0)
	attrData["magReCrit"] = _calAttr(petObj, "magReCrit", 0)
	
	return attrData

def _calAttr(petObj, attr, val=0, ratio=100):
	if attr in role.defines.baseAttrList:  # 基础属性
		attrPoint = "%sAllot" % attr # 手工分配的属性点
		val = petObj.fetch(attr) + petObj.fetch(attrPoint) + petObj.queryApply(attr)
	else:
		val = val + petObj.queryApply(attr)
	val = val * (ratio + petObj.queryApply("%sRatio" % attr)) / ratio
	return max(1, int(val))

def _calSkillApply(petObj):
	'''计算技能效果
	'''
	petObj.applyMgr.removeByPrefix("sk")
	skillList = petObj.getSkillList()
	for skillId, skillObj in skillList.iteritems():
		if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略低级技能
			continue
		skillObj.setup(petObj)


import role.defines
import skill
