# -*- coding: utf-8 -*-

def calcAttr(who):
	'''计算属性
	'''
	info = {
		"school":who.school,
		"level":who.level,
		"score":grade.gradeRole(who)
	}
	
	_calSkillApply(who)

	dSys = {}
	for attr in role.defines.baseAttrList:
		dSys[attr] = who.fetch(attr)
		
	dScheme = who.schemeCtn.getScheme().save()
	return _calcAttr2(info, dSys, dScheme, who.applyMgr)


def _calcAttr2(info, dSys, dScheme, applyObj):
	attrData = {}
	level = info["level"]

	# 基础属性
	attrData["con"] = con = _calAttr(applyObj, info, "con", dScheme.get('con', 0) + dSys["con"])
	attrData["mag"] = mag = _calAttr(applyObj, info, "mag", dScheme.get('mag', 0) + dSys["mag"])
	attrData["str"] = _str = _calAttr(applyObj, info, "str", dScheme.get('str', 0) + dSys["str"])
	attrData["res"] = res = _calAttr(applyObj, info, "res", dScheme.get('res', 0) + dSys["res"])
	attrData["spi"] = spi = _calAttr(applyObj, info, "spi", dScheme.get('spi', 0) + dSys["spi"])
	attrData["dex"] = dex = _calAttr(applyObj, info, "dex", dScheme.get('dex', 0) + dSys["dex"])
	
	# 主属性
	attrData["hpMax"] = _calAttr(applyObj, info, "hpMax", con * 8 + 50, 1000)
	attrData["mpMax"] = _calAttr(applyObj, info, "mpMax", mag * 1 + level * 5 + 200, 1000)
	attrData["spMax"] =  _calAttr(applyObj, info, "spMax", 150)
	attrData["huoliMax"] = _calAttr(applyObj, info, "huoliMax", 500 + level * 20)
	
	attrData["phyDam"] = _calAttr(applyObj, info, "phyDam", _str * 1 + 20 + level * 1)
	attrData["magDam"] = _calAttr(applyObj, info, "magDam", mag * 1 + 20 + level * 1)
	attrData["phyDef"] = _calAttr(applyObj, info, "phyDef", res * 2)
	attrData["magDef"] = _calAttr(applyObj, info, "magDef", spi * 2)
	attrData["spe"] = _calAttr(applyObj, info, "spe", con * 0.2 + mag * 0.2 + _str * 0.2 + res * 0.2 + spi * 0.2 + dex * 1.5)
	attrData["cure"] = _calAttr(applyObj, info, "cure", mag * 0.3 + 20 + level * 1)
	
	attrData["phyCrit"] = _calAttr(applyObj, info, "phyCrit", 3)
	attrData["magCrit"] = _calAttr(applyObj, info, "magCrit", 3)
	attrData["phyReCrit"] = _calAttr(applyObj, info, "phyReCrit", 0)
	attrData["magReCrit"] = _calAttr(applyObj, info, "magReCrit", 0)
	attrData["sealHit"] = _calAttr(applyObj, info, "sealHit", 0)
	attrData["reSealHit"] = _calAttr(applyObj, info, "reSealHit", 0)

	attrData["fightPower"] = info["score"]
	return attrData

def _calAttr(applyObj, info, attr, val=0, ratio=100):
	school = info["school"]
	level = info["level"]
	val = val + applyObj.query(attr)
	val += role.defines.getSchoolApply(school, attr) * level  # 门派额外附加
	val = val * (ratio + applyObj.query("%sRatio" % attr)) / ratio
	return max(0, int(val))

def _calSkillApply(who):
	'''计算技能效果
	'''
	who.applyMgr.removeByPrefix("sk")
	
	skillList = {}
	
	# 玩家技能
	skillList.update(who.getSkillList())
	
	#阵眼技能
	lineupObj = who.buddyCtn.getCurrentLineup()
	if lineupObj:
		eyeObj = lineupObj.getEyeObj()
		if eyeObj:
			skillList.update(eyeObj.getSkillList())

	for skillId, skillObj in skillList.iteritems():
		if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略低级技能
			continue
		skillObj.setup(who)


import role.defines
import grade
import skill
