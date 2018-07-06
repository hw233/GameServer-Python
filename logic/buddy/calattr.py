# -*- coding: utf-8 -*-

def transInfo(buddyObj):
	if not hasattr(buddyObj,"baseLevel") or buddyObj.baseLevel != buddyObj.level:
		buddyObj.attrInfo = getBaseInfo(buddyObj.id, buddyObj.level)
		buddyObj.baseLevel = buddyObj.level

	return buddyObj.attrInfo

def getBaseInfo(buddyNo, level):
	dBaseInfo  = buddyData.getBaseInfo(level)
	dBuddyInfo = buddyData.getBuddyInfo(buddyNo)
	attrInfo = {}

	for sKey,sVal in dBuddyInfo.iteritems():
		if sKey not in dBaseInfo:
			continue
		sVal = sVal.replace("B", "%s" % dBaseInfo[sKey])
		iVal = int(eval(sVal))
		attrInfo[sKey] = iVal

	return attrInfo
	
def calcAttr(buddyObj, level=0):
	'''计算属性
	'''
	attrData = {}

	_calSkillApply(buddyObj)
		
	# 主属性
	hpGen = buddyObj.getHpGen()
	phyAttGen = buddyObj.getPhyAttGen()
	magAttGen = buddyObj.getMagAttGen()
	phyDefGen = buddyObj.getPhyDefGen()
	magDefGen = buddyObj.getMagDefGen()
	speGen = buddyObj.getSpeGen()
	cureGen = buddyObj.getCureGen()

	if not level:
		attrInfo = transInfo(buddyObj)
	else:
		attrInfo = getBaseInfo(buddyObj.id, level)
	
	attrData["hpMax"] = _calAttr(buddyObj, "hpMax", attrInfo["生命"],hpGen)
	attrData["mpMax"] = _calAttr(buddyObj, "mpMax")
	
	attrData["phyDam"] = _calAttr(buddyObj, "phyDam",attrInfo["物理伤害"],phyAttGen)
	attrData["magDam"] = _calAttr(buddyObj, "magDam",attrInfo["法术伤害"],magAttGen)
	attrData["phyDef"] = _calAttr(buddyObj, "phyDef",attrInfo["物理防御"],phyDefGen)
	attrData["magDef"] = _calAttr(buddyObj, "magDef",attrInfo["法术防御"],magDefGen)
	attrData["spe"] = _calAttr(buddyObj, "spe",attrInfo["速度"],speGen)
	attrData["cure"] = _calAttr(buddyObj, "cure", attrInfo["治疗"], cureGen)
	
	attrData["phyCrit"] = _calAttr(buddyObj,"phyCrit")
	attrData["magCrit"] = _calAttr(buddyObj, "magCrit" )
	attrData["phyReCrit"] = _calAttr(buddyObj, "phyReCrit" )
	attrData["magReCrit"] = _calAttr(buddyObj, "magReCrit")
	attrData["sealHit"] = _calAttr(buddyObj, "sealHit",attrInfo["封印"])
	attrData["reSealHit"] = _calAttr(buddyObj, "reSealHit",attrInfo["抗封"])

	
	return attrData

def _calAttr(buddyObj, attr, val=0, ratio=1000):
	val = val + buddyObj.queryApply(attr)
	val = val * (ratio + buddyObj.queryApply("%sRatio" % attr)) / 1000
	return int(val)#max(1, int(val))

def _calSkillApply(buddyObj):
	'''计算技能效果
	'''
	buddyObj.applyMgr.removeByPrefix("sk")
	skillList = buddyObj.getValidSkillList()
	for skillId, skillObj in skillList.iteritems():
		if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略低级技能
			continue
		skillObj.setup(buddyObj)


import role.defines
import skill
import buddyData