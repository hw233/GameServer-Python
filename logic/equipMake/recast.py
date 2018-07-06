#-*-coding:utf-8-*-
#装备重铸

#数据保存在玩家身上，装备的临时变量在穿上/卸下、移入仓库/取回时会丢失
def setEquipRecastAttr(who, idx, recastAttr):
	'''保存重铸
	'''
	dEquipRecastAttr = getattr(who, "EquipRecastAttr", {})
	dEquipRecastAttr[idx] = recastAttr
	setattr(who, "EquipRecastAttr", dEquipRecastAttr)

def fetchEquipRecastAttr(who, id):
	dEquipRecastAttr = getattr(who, "EquipRecastAttr", {})
	return dEquipRecastAttr.get(id, {})

def delEquipRecastAttr(who, id):
	dEquipRecastAttr = getattr(who, "EquipRecastAttr", {})
	if dEquipRecastAttr.get(id, None):
		dEquipRecastAttr.pop(id, None)
		setattr(who, "EquipRecastAttr", dEquipRecastAttr)

def setEquipRecastTime(who, id):
	'''保存重铸时间
	'''
	dEquipRecastTime = getattr(who, "EquipRecastTime", {})
	dEquipRecastTime[id] = getSecond()
	setattr(who, "EquipRecastTime", dEquipRecastTime)

def fetchEquipRecastTime(who, id):
	dEquipRecastTime = getattr(who, "EquipRecastTime", {})
	return dEquipRecastTime.get(id, 0)

def delEquipRecastTime(who, id):
	dEquipRecastTime = getattr(who, "EquipRecastTime", {})
	if dEquipRecastTime.get(id, None):
		dEquipRecastTime.pop(id, None)
		setattr(who, "EquipRecastTime", dEquipRecastTime)

def getRecastEquip(who, propsId):
	'''只有包裹和穿上的装备能重铸
	'''
	oEquip = who.propsCtn.getItem(propsId)
	if not oEquip:
		oEquip = who.equipCtn.getItem(propsId)
	return oEquip


def getRecastCost(who, oEquip, quick=False):
	'''装备重铸所需材料 quick:是否使用快捷重铸
	'''
	dRecastNeed = oEquip.getConfig("重铸材料")
	propsNeeded = {}
	for iNo,iCount in dRecastNeed.iteritems():
		lPropsNo = equipMake.defines.getUpPropsNo(iNo)
		if not lPropsNo:
			propsNeeded[iNo] = iCount
			continue
		iHasPropNo = iNo
		for propsNo in lPropsNo:
			if sum(who.propsCtn.getPropsAmountByNos(propsNo)) >= iCount:
				iHasPropNo = propsNo
				break
		propsNeeded[iHasPropNo] = iCount

	if not quick:
		return propsNeeded

	#材料元宝价格，重铸石1000元宝，其它500元宝
	need = {}
	for propsNo, amount in propsNeeded.iteritems():
		amountHave = sum(who.propsCtn.getPropsAmountByNos(propsNo))
		if amount > amountHave:#材料不足，用元宝替换
			if amountHave > 0:
				need[propsNo] = amountHave
			ctype, price = trade.getGoodsPrice(propsNo)
			need[c.GOLD] = need.get(c.GOLD, 0) + (amount - amountHave)*price
		else:
			need[propsNo] = amount
	# print '=======getRecastCost======',propsNeeded,need
	return need

def checkReCastCost(who, propsNeeded):
	'''检查物品是否足够
	'''
	for propsNo, amount in propsNeeded.iteritems():
		if propsNo == c.GOLD:	#元宝
			if who.tradeCash < amount:
				return "元宝不足"
		else:
			amountHave = sum(who.propsCtn.getPropsAmountByNos(propsNo))
			if amount > amountHave:#材料不足
				oEquip = props.getCacheProps(propsNo)
				name = oEquip.name if oEquip else '{}'.format(propsNo)				
				return '{}不足{}'.format(name, amount)
	return ''

def doConsumeRecastCost(who, propsNeeded, reason):
	'''扣除物品
	'''
	for propsNo, amount in propsNeeded.iteritems():
		if propsNo == c.GOLD:	#元宝
			who.costTradeCash(amount, reason, None)
		else:
			who.propsCtn.subtractPropsByNo(propsNo, amount, reason, None)

def sendEquipRecastAttr(who, oEquip, iType=None):
	msg = {}
	if iType == None:
		if fetchEquipRecastAttr(who, oEquip.id):
			iType = 1
		else:
			iType = 0
	msg["iType"] = iType
	recastTime = fetchEquipRecastTime(who, oEquip.id)
	if recastTime:
		coolTime = int(math.ceil(recastTime + 3 - getSecond()))
		if coolTime > 0:
			msg["coolTime"] = coolTime 
		else:
			msg["coolTime"] = 0
			delEquipRecastTime(who, oEquip.id)
	else:
		msg["coolTime"] = 0
	msg["recastAttr"] = getEquipRecastAttrMsg(who, oEquip)
	# print msg
	who.endPoint.rpcEquipRecastResponse(**msg)

def getEquipRecastAttrMsg(who, oEquip):
	recastAttr = fetchEquipRecastAttr(who, oEquip.id)
	equipInfo = equipMake_pb2.equipInfo()
	equipInfo.iPropsId = oEquip.id
	equipInfo.iNo = oEquip.no()
	for name,attr in recastAttr.iteritems():
		if name not in ("spEffect", "spSkill", "isRare"):
			for k,v in attr.iteritems():
				setattr(equipInfo, k, v)

	equipInfo.isRare = recastAttr.get("isRare", 0)
	spEffect = recastAttr.get("spEffect", 0)
	if spEffect:
		equipInfo.spEffect = spEffect
	spSkill = recastAttr.get("spSkill", 0)
	if spSkill:
		equipInfo.spSkill = spSkill
	return equipInfo

def rpcEquipRecastAttr(who, reqMsg):
	'''获取装备重铸属性
	'''
	# print "======rpcEquipRecastAttr=========",reqMsg
	oEquip = getRecastEquip(who, reqMsg.propsId)
	if not oEquip:
		return
	if oEquip.kind != ITEM_EQUIP:
		return

	sendEquipRecastAttr(who, oEquip)

def rpcEquipRecast(who, reqMsg):
	'''装备重铸
	'''
	if who.level < 40:
		message.tips(who, "#C0440级#n开启#C02重铸系统#n")
		return
	oEquip = getRecastEquip(who, reqMsg.propsId)
	if not oEquip:
		return
	if oEquip.kind != ITEM_EQUIP:
		return

	# if not oEquip.fetch("addAttr") or not oEquip.getConfig("重铸材料"):
	if not oEquip.getConfig("重铸材料"):
		message.tips(who, "普通装备无法重铸")
		return

	#冷却时间
	recastTime = fetchEquipRecastTime(who, oEquip.id)
	if recastTime and getSecond() - recastTime < 3:
		message.tips(who, "冷却中,请#C04{}#n秒后再试".format(max(1, getSecond() - recastTime)))
		return

	propsNeeded = getRecastCost(who, oEquip, reqMsg.shortcut)
	# print "propsNeeded = ",propsNeeded
	if reqMsg.shortcut and propsNeeded.get(c.GOLD):
		if not money.checkTradeCash(who, propsNeeded.get(c.GOLD)):
			return
		# if who.tradeCash < propsNeeded.get(c.GOLD):
		# 	#检查游戏币是否足够
		# 	message.tips(who, "元宝不足")
		# 	return

	failReason = checkReCastCost(who, propsNeeded)
	if failReason:
		message.tips(who, failReason)
		#message.tips(who, "材料不足，无法重铸")
		return
	
	doConsumeRecastCost(who, propsNeeded, "装备重铸:{}".format(oEquip.no()))
	#重铸属性
	recastAttr = {}
	recastAttr["baseAttr"] = make.creatBaseAttr(oEquip)
	recastAttr["addAttr"] = make.creatAddAttr(oEquip)
	recastAttr["spEffect"] = make.createSpecialEffect(oEquip)
	recastAttr["spSkill"] = make.createSpecialSkill(oEquip)

	oEquipFork = props.fork(oEquip)
	oEquipFork.set("baseAttr", recastAttr["baseAttr"])
	oEquipFork.set("addAttr", recastAttr["addAttr"])
	oEquipFork.set("spEffect", recastAttr["spEffect"])
	oEquipFork.set("spSkill", recastAttr["spSkill"])

	#数据保存在玩家身上，装备的临时变量在穿上/卸下、移入仓库/取回时会丢失
	iIsRare = int(oEquipFork.isRare())
	recastAttr["isRare"] = iIsRare
	setEquipRecastAttr(who, oEquip.id, recastAttr)

	oldScore = oEquip.getScore()
	newScore = grade.gradeEquip(oEquipFork)
	# print "==rpcEquipRecast=",recastAttr,newScore,oldScore
	if newScore > oldScore or recastAttr.get("spEffect", 0) or recastAttr.get("spSkill", 0):
		setEquipRecastTime(who, oEquip.id)
	
	sendEquipRecastAttr(who, oEquip, 1)
	message.tips(who, "重铸成功")
	log.log("EquipRecast", "装备重铸:id={};no={};recastAttr={}".format(oEquip.id, oEquip.no(), recastAttr))
	
	import listener
	listener.doListen("重铸装备", who, propsNo=oEquip.no(), propsId=oEquip.id, recastIsRare=iIsRare)

def rpcEquipRecastReplace(who, reqMsg):
	'''重铸装备属性替换
	'''
	oEquip = getRecastEquip(who, reqMsg.propsId)
	if not oEquip:
		return
	if oEquip.kind != ITEM_EQUIP:
		return

	recastAttr = fetchEquipRecastAttr(who, oEquip.id)
	if not recastAttr:
		message.tips(who, "装备没有进行重铸属性")
		return

	#原有属性
	oldAttr = {}
	oldAttr["baseAttr"] = oEquip.fetch("baseAttr")
	oldAttr["addAttr"] = oEquip.fetch("addAttr")
	oldAttr["spEffect"] = oEquip.fetch("spEffect")
	oldAttr["spSkill"] = oEquip.fetch("spSkill")
	
	#替换属性
	baseAttr = recastAttr.get("baseAttr", {})
	addAttr = recastAttr.get("addAttr", {})
	spEffect = recastAttr.get("spEffect", 0)
	spSkill = recastAttr.get("spSkill", 0)
	oEquip.set("baseAttr", baseAttr)
	oEquip.set("addAttr", addAttr)
	oEquip.set("spEffect", spEffect)
	oEquip.set("spSkill", spSkill)

	delEquipRecastAttr(who, oEquip.id)
	delEquipRecastTime(who, oEquip.id)
	message.tips(who, "#C02{}#n成功替换新属性".format(oEquip.name))
	if oEquip.isWear():#穿上的装备
		who.endPoint.rpcModEquip(oEquip.getMsg4Item(who.equipCtn,*oEquip.MSG_ALL))
		oEquip.refreshApply(who)
	else:
		who.endPoint.rpcModProps(oEquip.getMsg4Package(who.propsCtn, *oEquip.MSG_ALL))
	sendEquipRecastAttr(who, oEquip, 2)
	log.log("EquipRecast", "重铸装备属性替换:id={};no={};oldAttr={};recastAttr={} ".format(oEquip.id, oEquip.no(), oldAttr, recastAttr))



import c
from props.defines import *
from common import *
import equipMake.defines
import message
import props
import make
import money
import common
import log
import grade
import equipMake_pb2
import math
import trade