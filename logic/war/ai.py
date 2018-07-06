# -*- coding: utf-8 -*-

SET_TYPE_ATTACK = 1 # 攻击集
SET_TYPE_HELP = 2 # 辅助集
SET_TYPE_SEAL = 3 # 封印集
SET_TYPE_RESEAL = 4 # 解封集
SET_TYPE_CURE = 5 # 治疗集

AISetTypeDesc = {
	"攻击集":SET_TYPE_ATTACK,
	"辅助集":SET_TYPE_HELP,
	"封印集":SET_TYPE_SEAL,
	"解封集":SET_TYPE_RESEAL,
	"治疗集":SET_TYPE_CURE,
}


def getPerform(att):
	if hasattr(att, "aiSetList"): # 使用自定义AI集
		aiSetList = att.aiSetList
	elif att.isBuddy(): # 使用伙伴AI集
		aiSetList = buddyAISetList[att.kind]
	else:
		return CMD_TYPE_PHY
	
	for setType in aiSetList:
		func = AISetTypeList[setType]
		performId = func(att)
		if performId:
			return performId

	return CMD_TYPE_PHY


#===============================================================================
# AI集
#===============================================================================

def AISetAttack(att):
	'''攻击集
	'''
	performObjListSingle = [] # 单攻法术
	performObjListMulti = [] # 群攻法术
	performTypeList = [PERFORM_TYPE_MAG, PERFORM_TYPE_PHY, PERFORM_TYPE_PHY_REMOTE]
	for performObj in getPerformList(att, *performTypeList):
		if performObj.isMultiTarget():
			performObjListMulti.append(performObj)
		else:
			performObjListSingle.append(performObj)
			
	if not (performObjListSingle or performObjListMulti):
		return 0
	
	performObj = None
	if len(att.getEnemyList()) > 1:
		if performObjListMulti:
			performObj = randPerform(att, performObjListMulti)
	else:
		if performObjListSingle:
			performObj = randPerform(att, performObjListSingle)
	
	if not performObj:
		performObjList = performObjListSingle + performObjListMulti
		performObj = randPerform(att, performObjList)

	return performObj.id

def AISetHelp(att):
	'''辅助集
	'''
	performObjList = getPerformList(att, PERFORM_TYPE_BUFF, PERFORM_TYPE_DEBUFF)
	if not performObjList:
		return 0
	
	tmpPerformObjList = performObjList
	performObjList = []
	warObj = att.war
	vic = None
	for performObj in tmpPerformObjList:
		if not vic:
			vic = warObj.getCommandTarget(att, performObj.id)
			if not vic: # 找不到攻击目标
				continue
		if getattr(performObj, "buffId", 0) and buff.has(vic, performObj.buffId):
			continue
		performObjList.append(performObj)
		
	if not performObjList:
		return 0
	
	att.targetIdx = vic.idx
	performObj = randPerform(att, performObjList)
	return performObj.id

def AISetSeal(att):
	'''封印集
	'''
	performObjList = getPerformList(att, PERFORM_TYPE_SEAL)
	if not performObjList:
		return 0
	
	targetList = []
	for w in att.getEnemyList():
		if w.inSeal():
			continue
		targetList.append(w)

	if not targetList:
		return 0
		
	vic = targetList[0]
	att.targetIdx = vic.idx
	performObj = randPerform(att, performObjList)
	return performObj.id

def AISetReSeal(att):
	'''解封集
	'''
	performObjList = getPerformList(att, PERFORM_TYPE_RESEAL)
	if not performObjList: # 没有解封法术
		return 0
	
	targetList = []
	for w in att.getFriendList():
# 		if not w.inSeal():
# 			continue
		inSeal = False
		for buffObj in w.buffList[BUFF_TYPEPOS_SEAL]:
			if not buffObj:
				continue
			if not buffObj.removable:
				continue
			inSeal = True
			break
		if inSeal:
			targetList.append(w)
		
	if not targetList: # 没有被封队员
		return 0
	targetList.sort(key=_sortKeyForReSeal)
	
	performId = 0
	if hasattr(att, "masterPerformList"):
		masterPerformList = att.masterPerformList
		for performObj in performObjList:
			if performObj.id in masterPerformList:
				performId = performObj.id
				
	if not performId and rand(100) < 20:
		performObj = performObjList[rand(len(performObjList))]
		performId = performObj.id
		
	if performId:
		vic = targetList[0]
		att.targetIdx = vic.idx
	return performId

def _sortKeyForReSeal(w):
	'''封集目标排序
	'''
	if w.isRole():
		return 1
	if w.isPet():
		return 2
	if w.isBuddy():
		if w.kind == "治疗型":
			return 3
		return 4
	return 99

def AISetCure(att):
	'''治疗集
	'''
	performObjListRevive = getPerformList(att, PERFORM_TYPE_REVIVE) # 复活技能
	performObjListCure = getPerformList(att, PERFORM_TYPE_CURE) # 治疗技能
	performObjListBuffMP = getPerformList(att, PERFORM_TYPE_BUFF_MP) # 增益真气技能
	if not (performObjListRevive or performObjListCure or performObjListBuffMP):
		return 0

	if performObjListRevive:
		performId = tryRevivePerform(att, performObjListRevive)
		if performId:
			return performId
	
	if performObjListCure:
		performId = tryCurePerform(att, performObjListCure)
		if performId:
			return performId
	
	if performObjListBuffMP:
		performId = tryBuffMPPerform(att, performObjListBuffMP)
		if performId:
			return performId

	return 0

def getPerformList(att, *performTypeList):
	'''获取法术列表
	'''
	performObjList = []
	for performObj in att.getPerformListByType(*performTypeList):
		if not performObj.validPerform(att, False):
			continue
		if not performObj.checkConsume(att):
			continue
		performObjList.append(performObj)
	return performObjList

def randPerform(att, performObjList, ratio=80):
	'''随机法术
	'''
	if len(performObjList) > 1 and hasattr(att, "masterPerformList") and rand(100) < ratio :
		masterPerformList = att.masterPerformList
		for performObj in performObjList:
			if performObj.id in masterPerformList:
				return performObj
			
	return performObjList[rand(len(performObjList))]

def getWarriorListByNotFullHP(att, isEnemy=False):
	'''获取生命未满战士
	'''
	if isEnemy:
		tmpWarriorList =  att.getEnemyList()
	else:
		tmpWarriorList = att.getFriendList()
		
	warriorList = []
	for w in tmpWarriorList:
		if w.hp < w.getHPMax():
			warriorList.append(w)
			
	return warriorList

def getWarriorListByNotFullMP(att, isEnemy=False):
	'''获取真气未满战士
	'''
	if isEnemy:
		tmpWarriorList =  att.getEnemyList()
	else:
		tmpWarriorList = att.getFriendList()
		
	warriorList = []
	for w in tmpWarriorList:
		if w.mp < w.getMPMax():
			warriorList.append(w)
			
	return warriorList

def getWarriorListByDead(att, isEnemy=False):
	'''获取死亡战士
	'''
	if isEnemy:
		tmpWarriorList =  att.getEnemyList(isAll=True)
	else:
		tmpWarriorList = att.getFriendList(isAll=True)
		
	warriorList = []
	for w in tmpWarriorList:
		if w.isDead():
			warriorList.append(w)
			
	return warriorList

def tryRevivePerform(att, performObjList):
	'''尝试复活法术
	'''
	warriorList = getWarriorListByDead(att)
	if not warriorList:
		return 0
	
	if hasattr(att, "masterPerformList"):
		masterPerformList = att.masterPerformList
		for performObj in performObjList:
			if performObj.id in masterPerformList:
				return performObj.id
	
	if rand(100) < 20:
		performObj = performObjList[rand(len(performObjList))]
		return performObj.id
	
	return 0
	

def tryCurePerform(att, performObjList):
	'''尝试治疗法术
	'''
	warriorList = getWarriorListByNotFullHP(att)
	if not warriorList:
		return 0
	
	performObj = randPerform(att, performObjList)
	return performObj.id
	

def tryBuffMPPerform(att, performObjList):
	'''尝试增益真气法术
	'''
	warriorList = getWarriorListByNotFullMP(att)
	if not warriorList:
		return 0
	
	performObj = performObjList[rand(len(performObjList))]
	return performObj.id


AISetTypeList = {
	SET_TYPE_ATTACK: AISetAttack,
	SET_TYPE_HELP: AISetHelp,
	SET_TYPE_SEAL: AISetSeal,
	SET_TYPE_RESEAL: AISetReSeal,
	SET_TYPE_CURE: AISetCure,
}

# 助战伙伴AI集
buddyAISetList = {
	"物攻型": (
		SET_TYPE_ATTACK,
		SET_TYPE_HELP,
		SET_TYPE_SEAL,
	),
	"法攻型": (
		SET_TYPE_ATTACK,
		SET_TYPE_HELP,
		SET_TYPE_SEAL,
	),
	"治疗型": (
		SET_TYPE_CURE,
		SET_TYPE_HELP,
		SET_TYPE_ATTACK,
	),
	"辅助型": (
		SET_TYPE_RESEAL,
		SET_TYPE_HELP,
		SET_TYPE_CURE,
		SET_TYPE_SEAL,
		SET_TYPE_ATTACK,
	),
	"封印型": (
		SET_TYPE_SEAL,
		SET_TYPE_ATTACK,
		SET_TYPE_HELP,
		SET_TYPE_CURE,
	),
}


from common import *
from war.defines import *
from perform.defines import *
from buff.defines import *
import buff