# -*- coding: utf-8 -*-

# =======================================================================
# 经验加成相关的
# =======================================================================

def getExpRatio(who):
	'''经验加成
	'''
	openLevel = getOpenLevel()
	realLevel = who.getRealLevel()
	expRatio = 100
	if realLevel - openLevel > 0 :
		expRatio = ratioByLevel.get(realLevel - openLevel,30)
	elif openLevel >= 73 and 37 <= realLevel <= openLevel-3:
		expRatio = min(200,(openLevel - realLevel - 2) * 5 + 100) #经验加成不能超过100%
	return expRatio

def checkExpRatio(who,bLogin=False):
	'''检查经验加成
	'''
	ratioBef = getattr(who,"ratio",100) #首次登陆
	ratioAft = getExpRatio(who)
	if not bLogin and ratioAft == ratioBef:
		return

	who.ratio = ratioAft

	if ratioAft > 100:  #经验加成
		who.expStateCtn.removeItem(EXP_DEC_STATE)
		if who.expStateCtn.getItem(EXP_ADD_STATE):
			who.expStateCtn.updateItem(EXP_ADD_STATE)
		else:
			who.expStateCtn.addItem(EXP_ADD_STATE)
	elif ratioAft == 100:
		who.expStateCtn.removeItem(EXP_DEC_STATE)
		who.expStateCtn.removeItem(EXP_ADD_STATE)
	else:  #经验衰减
		who.expStateCtn.removeItem(EXP_ADD_STATE)
		if who.expStateCtn.getItem(EXP_DEC_STATE):
			who.expStateCtn.updateItem(EXP_DEC_STATE)
		else:
			who.expStateCtn.addItem(EXP_DEC_STATE)


ratioByLevel = {
	1:50,
	2:50,
	3:40,
	4:40,
}

EXP_DEC_STATE = 105  #经验衰减状态
EXP_ADD_STATE = 106  #经验加成状态

# =======================================================================
# 服务器等级相关的
# =======================================================================
def checkOpenNewLevel(level):
	'''检查能否开启新等级
	'''
	parameter = block.parameter.parameter
	openLevel = parameter.getOpenLevel()
	if parameter.getOpenDay() or openLevel>=level:
		return

	day = openLevelData.getConfig(openLevel,"开启天数") + getDayNo()
	parameter.setOpenDay(day)

def getOpenLevel():
	'''开放等级
	'''
	return block.parameter.parameter.getOpenLevel()

def getOpenDay():
	'''开放天数
	'''
	parameter = block.parameter.parameter
	openDay = parameter.getOpenDay()
	if not openDay:
		return 0
	return openDay - getDayNo()

def openNewLevel(iYear,iMonth,iDay,iHour,iWeek):
	'''开启新等级
	'''
	parameter = block.parameter.parameter
	openDay = parameter.getOpenDay()
	if not openDay or openDay > getDayNo():
		return

	openLevel = parameter.getOpenLevel()
	newLevel = openLevelData.getConfig(openLevel,"开启等级") + openLevel

	parameter.setOpenLevel(newLevel)
	parameter.setOpenDay(0)
	role.callForAllRoles(checkExpRatio)

from common import *
import timerEvent
import openLevelData
import block.parameter
import state
import role
import gevent

def init():
	openNewLevel(1,2,3,4,5)
	timerEvent.geNewDay += openNewLevel