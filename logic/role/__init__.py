# -*- coding: utf-8 -*-

def getRole(roleId):
	return gKeeper.getObj(roleId)

def removeRole(roleId):
	'''角色下线
	'''
	gKeeper.removeObj(roleId)

import role.object
import role.roleKeeper
import factoryConcrete
import timer
import u
import config
import mainService
import log
import timingWheel
import timerEvent
import gevent

def onUpLevel(who):
	removeFromLevelList(who, who.level-1)
	addToLevelList(who)

def addToLevelList(who):
	lst = gdRoleIdByLevel.setdefault(who.level,[])
	if who.id not in lst:
		lst.append(who.id)

def removeFromLevelList(who, level=0):
	if not level:
		level = who.level
	lst = gdRoleIdByLevel.setdefault(level,[])
	if who.id in lst:
		lst.remove(who.id)

#===============================================================================
# 刷天、刷时时，玩家的处理
#===============================================================================

def callForAllRoles(func):
	'''为全部在线玩家调用函数
	'''
	roleList = gKeeper.getKeys()
	ti = 50
	per = len(roleList) / ti
	if len(roleList) % ti > (per / 2):
		per += 1

	for i in xrange(ti):
		idxBegin = i * per
		idxEnd = idxBegin + per
		if i == ti - 1:
			tmpList = roleList[idxBegin:]
		else:
			tmpList = roleList[idxBegin:idxEnd]
		
		if not tmpList:
			break
		
		tmpList = [v[0] for v in tmpList]
		gevent.spawn_later(i*0.1, _callBack, func, tmpList)

def _callBack(func, roleList):
	for pid in roleList:
		who = getRole(pid)
		if who:
			func(who)
			
def onNewDay(year, month, day, hour, wday):
	'''刷天时
	'''
	callForAllRoles(_onNewDay)

def _onNewDay(who):
	who.newDay()


if 'gbOnce' not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV:
		gKeeper=role.roleKeeper.cRoleKeeper(factoryConcrete.roleFtr)#主动登录上线的玩家才放到这个keeper
		geLogin=u.cEvent() #角色登录事件
		geReLogin=u.cEvent() #角色重新登录事件(执行登录流程时,角色对象已经在内存中,则为"重新登录")
		geOffLine=u.cEvent()
		geUpLevel=u.cEvent()
		geFightAbilityChange=u.cEvent()
		gdRoleIdByLevel = {}  #等级表，维护玩家等级

		if config.IS_INNER_SERVER:
			iScaleAmount,iInterval=30,1
		else:
			iScaleAmount,iInterval=60,10
		gTimingWheel=timingWheel.cTimingWheel(iScaleAmount,iInterval)#定时清理断线的角色
		
		timerEvent.geNewHour += onNewDay

