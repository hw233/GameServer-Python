# -*- coding: utf-8 -*-

def init():
	import perform.load

if "gPerformList" not in globals():
	gPerformList = {}

def new(pfId):
	'''创建法术
	'''
	import perform.load
	moduleList = perform.load.getModuleList()
	if pfId not in moduleList:
		raise Exception("找不到编号为%s的法术" % pfId)
	return moduleList[pfId].Perform()

def get(pfId):
	'''获取法术
	'''
	global gPerformList
	if pfId not in gPerformList:
		pfObj = new(pfId)
		gPerformList[pfId] = pfObj
	return gPerformList[pfId]

def isPassive(performId):
	'''是否被动法术
	'''
	performObj = get(performId)
	return performObj.isPassive()

def isSEPerform(performId):
	'''是否特技
	'''
	if (performId / 100) in (51, 52):
		return True
	return False

def summonMonster(att, monsterData, bout=0, replace=False):
	'''召唤怪物
	bout: 指定回合后消失，大于0才生效
	replace: 是否替换
	'''
	import war.monster
	import war.defines

	warObj = att.war
	side = att.side
	
	# 如果需要替换原来的，要先踢除
	if replace:
		for w in warObj.idxList.values():
			if hasattr(w, "summonIdx") and w.summonIdx == att.idx:
				warObj.kickWarrior(w)
				break
	
	monsterObj = war.monster.newMonster(monsterData)
	monsterObj.monsterIdx = 0
	monsterObj.monsterType = war.defines.MONSTER_TYPE_NORMAL
	
	monsterW = warObj.addMonsterFight(monsterObj, side)
	warObj.rpcAddWarrior(monsterW, None, True)
	warObj.rpcWarAllBuff(monsterW)
	
	monsterW.summonIdx = att.idx # 召唤出来的战士
	if bout > 0: # 指定回合后消失
		monsterW.boutMax = bout
	monsterW.addFunc("onEndRound", onEndRoundForSummon)
	return monsterW

def onEndRoundForSummon(w):
	'''召唤怪物在回合结束时的处理
	'''
	warObj = w.war
	if hasattr(w, "boutMax"): # 一定回合后消失
		if w.bout >= w.boutMax:
			warObj.kickWarrior(w)
