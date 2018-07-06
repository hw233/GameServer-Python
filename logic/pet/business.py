# -*- coding: utf-8 -*-
#
# 宠物业务相关逻辑
#
def autoAddPoint(petObj, refresh=True):
	curPoint = petObj.fetch("point")
	if curPoint < 10:
		return
	scheme = petObj.fetch("pointscheme")
	if not scheme:
		if petObj.level >= 40:
			return
		scheme = petPointAllot.getDefaultPointInfo(petObj.getConfig("类别"))
		if not scheme:
			return
	addTimes = curPoint / 10
	for attr in role.defines.baseAttrList:
		val = scheme.get(attr, 0)
		if val:
			petObj.addAttrPoint(attr, val*addTimes, "自动加点")
	petObj.addPoint(-10*addTimes, "自动加点")
	petObj.refreshAllotAttr(scheme.keys())
	petObj.reCalcAttr()

def learnSkill(who, petObj, sklId):
	'''学习技能 有几率顶替现有非特性技能
	'''
	dSklLst = petObj.getSkillList()
	lSpecSkl = petObj.getSpecialSKills()
	lSkills = dSklLst.keys()
	for skl in lSpecSkl:
		if skl in lSkills:# 一些异兽旧数据与新数据不一致
			lSkills.remove(skl)
	# 剩下的lSkills即是可以被顶替的技能
	shuffleList(lSkills)
	idx = rand(len(lSkills))
	replacedSkl = lSkills[idx]
	petObj.setSkill(replacedSkl, 0)
	petObj.setSkill(sklId, 1)
	return replacedSkl

def fillSkillSlotExp(petObj):
	'''升级满技能格所需的总剩余经验
	'''
	iNeed = 0
	iPoint = petObj.getSklPoint()
	iSklCnt = len(petObj.getSkillList())
	for i in xrange(1, iPoint+1):
		iNext = petSkillSlotsExp.getExp(iSklCnt+i)
		if iNext == -1:
			break
		iNeed += iNext
	iNeed -= petObj.getSklSlotExp()
	return max(0, iNeed)

def checkSkillBookUseCount(petObj, useCnt, skillExp):
	'''检查异兽消耗完潜力点所需的经验
	@useCnt:原计划要用的数量
	@skillExp:每个技能书增加的经验
	'''
	val = int(skillExp) * useCnt
	iNeed = fillSkillSlotExp(petObj)
	useCnt = min(useCnt, int(math.ceil(float(iNeed) / skillExp)))
	return useCnt, val

def canAddSkillSlot(petObj):
	'''是否能增加新技能格
	'''
	if petObj.getSklPoint() < 1:
		return False
	elif petObj.getSklSlotExpNxt() < 0:
		return False
	elif petObj.getSklSlotExp() < petObj.getSklSlotExpNxt():
		return False
	return True

def addRandomSkill(petObj):
	'''增加随机技能
	'''
	lSkillsLib = petWashData.gdRandomSkills.get("技能库", [])
	if not lSkillsLib:
		writeLog("pet/addRandomSkill", "unable to find the pet random skills library!")
		return
	lSkills = list(set(lSkillsLib) - set(petObj.getSkillList().keys()))
	shuffleList(lSkills)
	idx = rand(len(lSkills))
	sklId = lSkills[idx]
	petObj.setSkill(sklId, 1)
	writeLog("pet/addRandomSkill", "[%d]%d %d" % (petObj.ownerId, petObj.id, sklId))

def isWashed(petObj):
	'''是否洗炼过
	'''
	lGenExt = ["hpGenExt", "phyAttGenExt", "magAttGenExt", "phyDefGenExt", "magDefGenExt", "speGenExt"]
	for gen in lGenExt:
		if petObj.fetch(gen):
			return True
	return False

def hasWashNew(petObj):
	'''是否有新洗炼数据
	'''
	lNewGenExt = ["hpGenWashNew", "phyAttGenWashNew", "magAttGenWashNew", "phyDefGenWashNew", "magDefGenWashNew", "speGenWashNew", "sklPointWashNew"]
	for newExt in lNewGenExt:
		if petObj.fetch(newExt):
			return True
	return False

def checkStatus(petObj):
	'''检查是否达到变异的标准
	'''
	ptype = petObj.getConfig("类别")
	genList = pet.defines.genExtMaxNameList
	genListMin = pet.defines.genExtMinNameList
	genList2 = ["hpGenExt", "phyAttGenExt", "magAttGenExt", "phyDefGenExt", "magDefGenExt", "speGenExt"]
	level = 0
	exclude = None
	if ptype == 1:
		exclude = "phyAttGenExt"
		genExt = petObj.getConfig("额外物攻资质上限")
		genExtMin = petObj.getConfig("额外物攻资质最低值")
		level = int(math.ceil(float(petObj.fetch(exclude) - genExtMin) /  (genExt - genExtMin)* 6))
	elif ptype == 2:
		exclude = "magAttGenExt"
		genExt = petObj.getConfig("额外法攻资质上限")
		genExtMin = petObj.getConfig("额外法攻资质最低值")
		level = int(math.ceil(float(petObj.fetch(exclude) - genExtMin) /  (genExt - genExtMin)* 6))
	elif ptype == 3:
		exclude = "hpGenExt"
		genExt = petObj.getConfig("额外生命资质上限")
		genExtMin = petObj.getConfig("额外生命资质最低值")
		level = int(math.ceil(float(petObj.fetch(exclude) - genExtMin) /  (genExt - genExtMin)* 6))
	level = max(1, level)
	speciQuaGra = petVariationData.getConfig(ptype, "特长资质档次")
	otherGraSum = petVariationData.getConfig(ptype, "其余档次总和")
	if level < speciQuaGra:
		return
	level = 0
	for idx, gen in enumerate(genList2):
		if exclude == gen:
			continue
		cnGen = genList[idx]
		cnGen2 = genListMin[idx]
		genExt = petObj.getConfig(cnGen)
		genExtMin = petObj.getConfig(cnGen2)
		level += max(1, int(math.ceil(float(petObj.fetch(gen) - genExtMin) /  (genExt - genExtMin)* 6)))
	if level < otherGraSum:
		return
	petObj.addSklPoint(2, "增加技能格", False)
	petObj.set("status", 1)
	petObj.setColors({role.defines.SHAPE_PART_TYPE_BODY:2}) # 目前写死变异的默认方案为2
	message.tips(petObj.getOwnerObj(), "恭喜你！当前异兽已成#C04凝神#n状态！")

def updateExtGenDirect(petObj, dWashAttr):
	'''直接根据字典的数据更新额外资质
	'''
	dGenMap = {
	"hpGenExt" : "hpGenWashNew",
	"phyAttGenExt" : "phyAttGenWashNew",
	"magAttGenExt" : "magAttGenWashNew",
	"phyDefGenExt" : "phyDefGenWashNew",
	"magDefGenExt" : "magDefGenWashNew",
	"speGenExt" : "speGenWashNew",
	"sklPoint" : "sklPointWashNew"
	}
	for gen, genNew in dGenMap.iteritems():
		petObj.set(gen, dWashAttr.get(genNew))
	petObj.reCalcAttr()
	# 检查是否洗炼出变异
	if not petObj.fetch("status"):
		checkStatus(petObj)
	petObj.attrChange("score","hpGen","phyAttGen","magAttGen","phyDefGen","magDefGen","speGen", "sklPoint",
		"hpGenExt", "phyAttGenExt", "magAttGenExt", "phyDefGenExt", "magDefGenExt", "speGenExt", "status", "sklSlotExpAll")

def updateExtGen(petObj):
	'''将洗炼属性更新到正式属性中
	'''
	dGenMap = {
	"hpGenExt" : "hpGenWashNew",
	"phyAttGenExt" : "phyAttGenWashNew",
	"magAttGenExt" : "magAttGenWashNew",
	"phyDefGenExt" : "phyDefGenWashNew",
	"magDefGenExt" : "magDefGenWashNew",
	"speGenExt" : "speGenWashNew",
	"sklPoint" : "sklPointWashNew"
	}
	# 将原来刷的额外资质保存到OLD里面
	petObj.set("hpGenWashOld", petObj.fetch("hpGenExt"))
	petObj.set("phyAttGenWashOld", petObj.fetch("phyAttGenExt"))
	petObj.set("magAttGenWashOld", petObj.fetch("magAttGenExt"))
	petObj.set("phyDefGenWashOld", petObj.fetch("phyDefGenExt"))
	petObj.set("magDefGenWashOld", petObj.fetch("magDefGenExt"))
	petObj.set("speGenWashOld", petObj.fetch("speGenExt"))
	petObj.set("sklPointOld", petObj.fetch("sklPoint"))
	# 将洗炼出来的额外资质保存到正式属性里面
	for gen, genNew in dGenMap.iteritems():
		petObj.set(gen, petObj.fetch(genNew))
		petObj.set(genNew, 0)
	petObj.reCalcAttr()
	# 检查是否洗炼出变异
	if not petObj.fetch("status"):
		checkStatus(petObj)
	petObj.attrChange("score","hpGen","phyAttGen","magAttGen","phyDefGen","magDefGen","speGen", "sklPoint",
		"hpGenExt", "phyAttGenExt", "magAttGenExt", "phyDefGenExt", "magDefGenExt", "speGenExt", "status", "sklSlotExpAll")

def wash(petObj):
	'''洗炼
	'''
	dWashAttr = {
	"hpGenWashNew" : 0,
	"phyAttGenWashNew" : 0,
	"magAttGenWashNew" : 0,
	"phyDefGenWashNew" : 0,
	"magDefGenWashNew" : 0,
	"speGenWashNew" : 0,
	"sklPointWashNew" : 0
	} # 洗炼属性字典
	genList = pet.defines.genExtMaxNameList
	genListMin = pet.defines.genExtMinNameList
	for idx, gen in enumerate(genList):
		genExt = petObj.getConfig(gen)
		genExtMin = petObj.getConfig(genListMin[idx])
		level = chooseKey(petWashData.gdGrowLevelRate, key="几率")	#档次，1档对应取0~1档间的随机值
		if petObj.fetch("status") == 1:
			level += 1
		average = float(genExt - genExtMin) / 6	#每档数值范围
		start = genExtMin + average * (level - 1)	# 档次数值起点
		res = int(start + average * rand(0, 100) / 100.0)	# 最终的取值
		dWashAttr[pet.defines.washDescList[gen]] = res
	skillCnt = len(petObj.getSkillList()) - len(petObj.getSpecialSKills())
	maxPoint = 8 if petObj.fetch("status") else 6
	dWashAttr["sklPointWashNew"] = max(0, maxPoint - skillCnt)
	return dWashAttr


import math
import role.defines
import pet.defines
from common import *
import petWashData
import petSkillSlotsExp
import message
import petVariationData
import petPointAllot
