# -*- coding: utf-8 -*-
import skillSchData

OK = 0
ERR_TOP_LEVEL = -1
ERR_LACK_CASH = -2

#===============================================================================
# 职业技能相关
#===============================================================================
def checkSchSkillOpen(who):
	'''检查职业技能开启
	'''
	updated = False
	skillList = skillSchData.getOpenSchSkill(who.school, who.level)
	for skId in skillList:
		if who.querySkillLevel(skId):
			continue
		who.setSkill(skId, 1)
		updated = True
		writeLog("skill/skillopen", "%d %d" % (who.id, skId))
		
	if updated:
		who.reCalcAttr()

def doSkillSchUpgrade(who, skId):
	'''升级
	'''
	skObj = who.skillCtn.getItem(skId)
	if not skObj:
		return
	level = skObj.level
	tRet = calcUpgradeSkillSch(who, skId, level, skObj.getLevelMax(who))
	errCode = tRet[0]
	cost = tRet[1]
	add = tRet[2]
	if errCode == ERR_LACK_CASH:
		if not money.checkCash(who, cost):
			return
	elif errCode == ERR_TOP_LEVEL:
		message.tips(who, "门派技能无法超过人物等级")
		return
	who.costCash(cost, "升级技能%d"%skId)
	writeLog("skill/upgrade", "%d %d %d %d->%d" % (who.id, skId, cost, level, level+add))
	who.setSkill(skId, level + add)
	who.reCalcAttr()
	
	import listener
	listener.doListen("升级门派技能", who)

def calcUpgradeSkillSch(who, skId, level, levelMax, realCost=0):
	# 返回：(错误码,费用,提升等级)
	if level >= levelMax:
		return ERR_TOP_LEVEL, 0, 0
	cost = calcSkillSchCost(skId, level)
	if who.cash < cost + realCost:
		return ERR_LACK_CASH, cost, 1
	return OK, cost, 1

def upgradeSkillSch(who, skObj, isRepeat=False):
	skId = skObj.id
	level = skObj.level
	levelMax = skObj.getLevelMax(who)
# 	skIdBase = getBaseSkill(who.school)
	if level >= levelMax:
		return
# 	if skId != skIdBase and level >= who.querySkillLevel(skIdBase): # 策划说没有基础技能
# 		return
	
	cost = calcSkillSchCost(skId, level)
	if isRepeat:
		add = levelMax - level
	else:
		add = 1
	
	if who.cash < cost * add:
		add = who.cash / cost
		if add < 1:
			return

	# 扣费用
	cost = cost * add
	who.costCash(cost, "升级技能%d"%skId)
	writeLog("skill/upgrade", "%d %d %d %d->%d" % (who.id, skId, cost, level, level+add))
	who.setSkill(skId, level + add)
	who.reCalcAttr()

def doCheckCash(who, skillList):
	'''判断一键升级是否需要弹出银币不足
	'''
	iTotalCost = calcSkillSchTotalCost(who, skillList)
	iLen = len(skillList)
	# 先模拟循环一次，如果因为银币不足一个都不能升级，则弹出银币不足接口
	iCheckCash = 0
	for skObj in skillList:
		tRet = calcUpgradeSkillSch(who, skObj.id, skObj.level, skObj.getLevelMax(who))
		if tRet[0] == ERR_LACK_CASH:
			iCheckCash += 1
	# 一个都不能升级的情况
	if iCheckCash == len(skillList):
		if not money.checkCash(who, iTotalCost):
			return False
	return True

def doSkillSchUpgradeLoop(who, skillList, iRepeat):
	'''所有已解锁的技能按解锁等级逐个进行等级+1的升级
	当所有可升级的技能等级都+1后，再次进行上一条
	'''
	dTmp = {skill.id:(0, 0) for skill in skillList}
	iRealCost = 0
	iLen = len(skillList)
	for i in xrange(iRepeat):
		iCheckCash = 0
		for skObj in skillList:
			skId = skObj.id
			oldValue = dTmp.get(skId, (0, 0))
			tRet = calcUpgradeSkillSch(who, skObj.id, skObj.level+oldValue[0], skObj.getLevelMax(who), iRealCost)
			if tRet[0] != OK:
				iCheckCash += 1
			else:
				iRealCost += tRet[1]
				dTmp[skId] = (oldValue[0]+tRet[2], oldValue[1]+tRet[1])
		# 一直循环到本轮技能都不能升级为止
		if iCheckCash == iLen:
			break
	return iRealCost, dTmp

def doSkillSchUpgradeAll(who):
	'''一键升级
	'''
	skillList = getCanUpgradeSkillList(who)
	if not skillList:
		message.tips(who, "门派技能等级都已达到上限，提升人物等级可提高该上限")
		return
	skillList.sort(key=lambda skObj:skObj.level)
	iRepeat = who.level - skillList[0].level
	skillList.sort(key=lambda skObj:skObj.getOpenLevel())
	if not doCheckCash(who, skillList):
		return
	iRealCost, dTmp = doSkillSchUpgradeLoop(who, skillList, iRepeat)
	# 扣费用
	who.costCash(iRealCost, "一键升级门派技能")
	for skObj in skillList:
		skId = skObj.id
		oldLevel = skObj.level
		addLevel, cost = dTmp.get(skId, 0)
		if not addLevel:
			continue
		writeLog("skill/upgrade", "%d %d %d %d->%d" % (who.id, skId, cost, oldLevel, oldLevel+addLevel))
		who.setSkill(skId, oldLevel + addLevel)
	who.reCalcAttr()
	message.tips(who, "一键升级成功")
	
	import listener
	listener.doListen("升级门派技能", who)

def getBaseSkill(sch):
	'''职业基础技能
	'''
	return 1011 + sch * 100

def getCanUpgradeSkillList(who):
	'''获取可升级的技能列表
	'''
	skillList = []
	for skObj in who.skillCtn.getAllValues():
		if not hasattr(skObj, "school"): # 非职业技能
			continue
		if skObj.level >= skObj.getLevelMax(who):
			continue
		skillList.append(skObj)
	return skillList

def calcSkillSchCost(skId, level):
	'''费用
	'''
	if 1111 <= skId < 3000: # 职业技能
		return skillSchUpgrade.getCostByLevel(level) 
	return 999999

def calcSkillSchTotalCost(who, skillList):
	'''升级列表里的技能所需的费用
	'''
	iTotalCost = 0
	for skObj in skillList:
		skId = skObj.id
		level = skObj.level
		levelMax = skObj.getLevelMax(who)
		while level < levelMax:
			iTotalCost += calcSkillSchCost(skId, level)
			level += 1
	return iTotalCost


#===============================================================================
# 学习帮派技能相关
#===============================================================================
def doSkillGuildLearn(who, skId):
	'''学习帮派技能
	'''
# 	guildObj = who.guild
# 	if not guildObj:
# 		# toDo 弹出加入帮派界面
# 		return
	if who.level < 15:
		return
	# elif not who.getGuildObj():
	# 	message.tips(who, "你的帮贡处于冻结状态，需要加入帮派才能使用")
	# 	return
	skObj = skill.get(skId)
	skName = skObj.name
	lastLevel = who.querySkillLevel(skId)
	level = lastLevel + 1
	if level > skObj.getLevelMax(who):
		message.tips(who, "继续学习#C02%s#n需要#C04%d级#n" % (skName, who.level+1))
		# message.tips(who, "学习#C03%d级%s#n需要#C03%d级#n" % (level, skName, who.level+1))
		return
		
	costData = calSkillGuildLearnCost(skId, level)
	costCash = costData["银币"]
	costGuildPoint = costData["帮贡"]
	if who.cash < costCash:
		# message.tips(who, "学习#C02%d级%s#n需要帮贡#C02%d点#n" % (level, skName, costCash))
		#toDo 进入银币不足界面
		if not money.checkCash(who, costCash):
			return
		# return
	if who.fetch("guildPoint") < costGuildPoint:
		message.tips(who, "学习#C04{}级#n#C02{}#n需要仙盟贡献#R<{},7,2>#n#C02点#n".format(level, skName, costGuildPoint))
		return
	
	writeLog("skill/learn", "%d %d %d->%d cost %d %d" % (who.id, skId, lastLevel , level, costCash, costGuildPoint))
	who.costCash(costCash, "学习帮派技能", None)
	if costGuildPoint:
		who.addGuildPoint(-costGuildPoint, "学习帮派技能")
	who.setSkill(skId, level)
	who.reCalcAttr()
	message.tips(who, "消耗#IS#n#C02{:,}#n，将#C02{}#n提升至#C04{}#n级".format(costCash, skName, level))
	
def calSkillGuildLearnCost(skId, level):
	'''学习帮派技能费用
	'''
	costData = {}
	for costType in ("银币", "帮贡",):
		val = skillGuildData.getConfig(skId, costType)
		baseVal = skillGuildLearn.getConfig(level, costType)
		val = val.replace("B", str(baseVal))
		costData[costType] = int(eval(val))
	return costData


#===============================================================================
#使用帮派技能相关
#===============================================================================
def doSkillGuildUse(who, skId, skLv):
	'''使用帮派技能
	'''
	useFunc = skillGuildUseHandler.get(skId)
	if not useFunc:
		return
	
	level = who.querySkillLevel(skId)
	if not level:
		return
	skObj = skill.new(skId)
	skObj.level = level
	useFunc(who, skObj, skLv)

def calSkillGuildUseCost(skId, level):
	'''使用帮派技能消耗
	'''
	costData = {}
	for costType in ("活力", ):
		val = skillGuildData.getConfig(skId, costType)
		val = val.replace("LV", str(level))
		costData[costType] = int(eval(val))
	return costData

def makeFood(who, skObj, skLv=0):
	'''厨艺
	'''
	if who.propsCtn.leftCapacity() < 1:
		message.tips(who, "背包已满，请先清理背包")
		return
	costData = calSkillGuildUseCost(skObj.id, skObj.level)
	costHuoli = costData["活力"]
	if who.huoli < costHuoli:
		message.tips(who, "活力不足，无法烹饪" )
		return
	
	data = makeFoodData.getConfig(skObj.level)
	propsNoList = data["物品"]
	propsNo = propsNoList[rand(len(propsNoList))]
	quality = 0
	if propsNo in (220001,):
		propsObj = props.new(propsNo)
	else:
		quality = skObj.getEffectVal(who) # 品质
		propsObj = props.new(propsNo, quality=quality)
	
	writeLog("skill/makefood", "%d get %d(%d) cost %d" % (who.id, propsNo, quality, costHuoli))
	who.addHuoli(-costHuoli, "厨艺")
	launch.launchProps(who, propsObj, "厨艺", None)
	qualityStr = "#C04%d#n品质的" % propsObj.quality if propsNo != 220001 else ""
	message.tips(who, "$P<1,0.4,%s>#n烹饪成功，获得1个%s#C02%s#n" % (propsNo, qualityStr, propsObj.name))
	message.message(who,"你获得了#C02%s#n" % propsObj.name)

def makeMedicine(who, skObj, skLv=0):
	'''炼丹
	'''
	if who.propsCtn.leftCapacity() < 1:
		message.tips(who, "背包已满，请先清理背包")
		return
	costData = calSkillGuildUseCost(skObj.id, skObj.level)
	costHuoli = costData["活力"]
	if who.huoli < costHuoli:
		message.tips(who, "活力不足，无法炼丹")
		return

	data = makeMedicineData.getConfig(skObj.level)
	propsNo = chooseKey(data)
	quality = 0

	if propsNo in (221001, 221002,):
		propsObj = props.new(propsNo)
		tips = "$P<1,0.4,%s>#n炼丹失败，获得1个#C02%s#n" % (propsNo, propsObj.name)
	else:
		quality = max(skObj.getEffectVal(who),1) # 品质,保底1
		propsObj = props.new(propsNo, quality=quality)
		tips = "$P<1,0.4,%s>#n炼丹成功，获得1个#C04%d#n品质的#C02%s#n" % (propsNo, quality,propsObj.name)
	
	writeLog("skill/makeMedicine", "%d get %d(%d) cost %d" % (who.id, propsNo, quality, costHuoli))
	who.addHuoli(-costHuoli, "炼丹")
	launch.launchProps(who, propsObj, "炼丹", None)
	message.tips(who, tips)
	message.message(who,"你获得了#C02%s#n" % propsObj.name)
	
def makeMaterial(who, skObj, skLv):
	'''制作材料符(打造符、裁缝符、炼金符)
	'''
	if who.propsCtn.leftCapacity() < 1:
		message.tips(who, "背包已满，请先清理背包")
		return
	costData = calSkillGuildUseCost(skObj.id, skLv)
	costHuoli = costData["活力"]
	if who.huoli < costHuoli:
		message.tips(who, "活力不足，无法制作")
		return
	
	propsNo = getMaterial(skObj.id, skLv)
	if who.querySkillLevel(skObj.id) < 40:
		message.tips(who, "制作#C02{}#n需要#C02{}#n#C04≥40级#n".format(props.getPropsName(propsNo), skObj.name))
		return 

	propsObj = props.new(propsNo)
	
	writeLog("skill/makematerial", "%d get %d cost %d" % (who.id, propsNo, costHuoli))
	who.addHuoli(-costHuoli, skObj.name)
	launch.launchProps(who, propsObj, skObj.name, None)
	message.tips(who, "$P<1,0.4,%s>#n制作成功，获得1个#C02%s#n" % (propsNo, propsObj.name))
	message.message(who,"你获得了#C02%s#n" % propsObj.name)
	
def getMaterial(skId, level):
	'''技能对应的材料符
	'''
	# 材料符从10级开始，故level最少应该为10
	level = max(level, 10)
	propsNo = skillGuildData.getConfig(skId, "效果物品")
	propsNo = propsNo.replace("LV", str(level))
	return int(eval(propsNo))

# 使用帮派技能的处理函数
skillGuildUseHandler = {
	503: makeFood,
	504: makeMedicine,
	505: makeMaterial,
	506: makeMaterial,
	507: makeMaterial,
}


#===============================================================================
#使用修炼相关
#===============================================================================
CASH_ONE_TIME = 20000 #一次消耗的金钱


def doSkillPracticeLearn(who, skId, learnType):
	'''学习修炼技能
	'''
	if skId not in (6101,6102,6103,6104,6105,6106,6107,6108):
		return

	maxLevel = checkAndGetPracticeLevel(who,skId)
	if not maxLevel:
		return
	if not checkPracticeCost(who,learnType):
		return

	func = practiceByType.get(learnType)
	if func:
		func(who,skId,maxLevel)

def checkPracticeCost(who,learnType):
	'''检查金钱
	'''
	costCash = 0
	if learnType == 1:
		costCash = CASH_ONE_TIME
	elif learnType == 2:
		costCash = CASH_ONE_TIME * 10

	return money.checkCash(who,costCash)

def checkAndGetPracticeLevel(who,skId):
	'''获取修炼等级上限
	'''
	lastLevel = who.querySkillLevel(skId)
	guildLevel = who.getPracticeGuildLevel()
	roleLevel = who.getPracticeRoleLevel()
	guildPoint = who.getPracticeGuildPoint()
	maxLevel = min(guildLevel,roleLevel,guildPoint)

	if lastLevel < maxLevel:
		return maxLevel

	lst = []
	if maxLevel == roleLevel:
		lst.append("等级")
	if maxLevel == guildLevel:
		lst.append("帮派等级")
	if maxLevel == guildPoint:
		lst.append("历史帮贡")

	message.tips(who,"你的修炼已达上限，请提升#C04%s#n" % "、".join(lst))
	return 0

def practiceOne(who,skId,maxLevel):
	'''修炼一次
	'''
	oldLevel = who.skillCtn.getLevel(skId)
	who.costCash(CASH_ONE_TIME,"修炼",None)
	who.skillCtn.addPracticePoint(skId,10)
	sendMessage(who,skId,oldLevel,10)
	
def practiceTen(who,skId,maxLevel):
	'''修炼十次
	'''
	times = 10
	skObj = who.skillCtn.getItem(skId)
	oldLevel = who.skillCtn.getLevel(skId)
	if skObj and skObj.level == maxLevel-1:
		needPoint = skObj.getPointNext()-skObj.getPoint()
		times = min(times,needPoint/10)

	who.costCash(CASH_ONE_TIME*times,"修炼",None)
	who.skillCtn.addPracticePoint(skId,10*times)
	sendMessage(who,skId,oldLevel,10*times)

def practiceByProps(who,skId,maxLevel):
	'''使用道具修炼
	'''
	propsNo = 202024 if skId in (6101,6102,6103,6104) else 202025
	amount, = who.propsCtn.getPropsAmountByNos(propsNo)
	if not amount:
		propsObj = props.getCacheProps(propsNo)
		message.tips(who,"你的%s不足" % propsObj.name)
		return
	oldLevel = who.skillCtn.getLevel(skId)
	skObj = who.skillCtn.getItem(skId)
	if not skObj:
		skObj = skill.get(skId)
		needPoint = skillPraticeLevelData.getPointNext(skObj.name,1)
	else:
		needPoint = skObj.getPointNext()-skObj.getPoint()

	amount = min(amount,needPoint/10)
	who.propsCtn.subPropsByNo(propsNo,amount,"修炼")
	who.skillCtn.addPracticePoint(skId,10*amount)
	sendMessage(who,skId,oldLevel,10*amount)

def sendMessage(who,skId,oldLevel,point):
	message.tips(who,"获得#C02%d#n点修炼经验" % point)
	skObj = who.skillCtn.getItem(skId)
	if skObj.level > oldLevel:
		message.tips(who,"#C02%s#n提升到#C04%d#n级" % (skObj.name,skObj.level))

practiceByType = {
	1:practiceOne,
	2:practiceTen,
	3:practiceByProps,
}

# def doSkillMakeMedicine(who, skObj, propsIdList):
# 	'''炼丹.消耗药材
# 	'''
# 	costData = calSkillGuildUseCost(skObj.id, skObj.level)
# 	makeMedicine(who, skObj, propsIdList, costData)
	
# def doSkillMakeMedicineByCash(who, skObj):
# 	'''炼丹.消耗银币
# 	'''
# 	propsIdList = []
# 	costData = calSkillGuildUseCost(skObj.id, skObj.level)
# 	costData["银币"] = 6000
# 	makeMedicine(who, skObj, propsIdList, costData)

# def makeMedicine(who, skObj, propsIdList, costData):
# 	if not checkForMakeMedicine(who, propsIdList, costData):
# 		return
	
# 	isSuccess, propsObj = produceProps(who, propsIdList, skObj)
# 	if propsObj:
# 		propsNo = propsObj.no()
# 		quality = getattr(propsObj, "quality", 0)
# 	else:
# 		propsNo = 0
# 		quality = 0
	
# 	costMsg = ",".join(["%s=%s"%(k,v) for k,v in costData.iteritems()])
# 	writeLog("skill/makemedicine", "%d get %d(%d) cost %s" % (who.id, propsNo, quality, costMsg))
# 	resumeForMakeMedicine(who, propsIdList, costData)
		
# 	if propsObj:
# 		launch.launchProps(who, propsObj, "炼丹", None)
# 		if isSuccess:
# 			message.tips(who, "$P<1,0.6,%s>#n炼丹成功，获得1个#C3$%d#n品质的#C3%s#n" % (propsNo,quality,propsObj.name))
# 		else:
# 			message.tips(who, "$P<1,0.6,%s>#n炼丹成功，获得1个#C3%s#n" % (propsNo,propsObj.name))
# 	else:
# 		message.tips(who, "炼丹失败")

# 	who.endPoint.rpcSkillMedicineResult(isSuccess)

# def checkForMakeMedicine(who, propsIdList, costData):
# 	'''检查炼丹
# 	'''
# 	# 检查消耗
# 	costHuoli = costData.get("活力")
# 	if costHuoli and who.huoli < costHuoli:
# 		message.tips(who, "炼丹需要活力#C3%d点#n" % costHuoli)
# 		return 0
# 	costCash = costData.get("银币")
# 	if costCash and who.cash < costCash:
# 		message.tips(who, "炼丹需要银币#C3%d#n" % costCash)
# 		return 0
	
# 	# 检查炼丹材料
# 	if propsIdList:
# 		for propsId, amount in propsIdList.iteritems():
# 			propsObj = who.propsCtn.getItem(propsId)
# 			if not propsObj:
# 				message.tips(who, "请放入炼丹材料")
# 				return 0
# 			if propsObj.stack() < amount:
# 				message.tips(who, "你身上没有这么多的%s" % propsObj.name)
# 				return 0
# 			if propsObj.kind != ITEM_MEDICINE_LEVEL or propsObj.level not in (1, 2,):
# 				message.tips(who, "请放入炼丹材料")
# 				return 0

# 	return 1
	
# def produceProps(who, propsIdList, skObj):
# 	'''炼丹产出物品
# 	'''
# 	isSuccess = 0
# 	modeData = getModeData(who, propsIdList)
# 	if rand(100) >= modeData["成功率"]:
# 		propsNoList = modeData.get("失败", [])
# 	else:
# 		isSuccess = 1
# 		propsNoList = modeData["成功"]
	
# 	propsObj = None
# 	if propsNoList:
# 		propsNo = propsNoList[rand(len(propsNoList))]
# 		if propsNo in (221001, 221002,):
# 			propsObj = props.new(propsNo)
# 		else:
# 			quality = skObj.getEffectVal(who) # 品质
# 			propsObj = props.new(propsNo, quality=quality)
			
# 	return isSuccess, propsObj
	
# def getModeData(who, propsIdList):
# 	'''获取匹配的炼丹模式数据
# 	'''
# 	mode = {}
# 	if propsIdList:
# 		for propsId, amount in propsIdList.iteritems():
# 			propsObj = who.propsCtn.getItem(propsId)
# 			level = propsObj.level
# 			mode[level] = mode.get(level, 0) + amount
# 	else:
# 		mode = {1:4,}
# 	return makeMedicineData.getConfig(mode)
		
# def resumeForMakeMedicine(who, propsIdList, costData):
# 	'''消耗
# 	'''
# 	if propsIdList:
# 		for propsId, amount in propsIdList.iteritems():
# 			propsObj = who.propsCtn.getItem(propsId)
# 			who.propsCtn.addStack(propsObj, -amount)
	
# 	if costData.get("活力"):
# 		who.addHuoli(-costData["活力"], "炼丹")
# 	if costData.get("银币"):
# 		who.costCash(costData["银币"], "炼丹", None)


from common import *
from props.defines import *
import message
import skill
import launch
import props
import skillSchUpgrade
import skillGuildData
import skillGuildLearn
import makeFoodData
import makeMedicineData
import money
import skillPraticeLevelData