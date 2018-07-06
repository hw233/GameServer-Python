# -*- coding: utf-8 -*-
'''活动相关
'''
def init():
	print "activity init..."
	timerEvent.geNewHour += onNewHour
	timerEvent.geNewWeek += onNewWeek
	global gActivityList
	for activityId in activity.load.activityInfoList.iterkeys():
		obj = gActivityKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY, activityId)
		gActivityList[obj.name] = obj
		obj.init()
		
def create(activityId):
	info = activity.load.activityInfoList[activityId]
	mod = info["mod"]
	name = info["name"]
	obj = mod.Activity(activityId, name)
	return obj

def getActivity(name):
	return gActivityList.get(name)

def onNewWeek(year, month, day, hour, wday):
	'''系统刷周时
	'''
	for obj in gActivityList.itervalues():
		if hasattr(obj, "onNewWeek"):
			obj.onNewWeek(year,month,day,hour,wday)

def onNewHour(year, month, day, hour, wday):
	'''系统刷小时时
	'''
	for obj in gActivityList.itervalues():
		if hasattr(obj, "onNewHour"):
			obj.onNewHour(day, hour, wday)

def onNewDay(who):
	'''玩家刷天时
	'''
	for obj in gActivityList.itervalues():
		if hasattr(obj, "onNewDay"):
			obj.onNewDay(who)
		
def onUpLevel(who):
	'''玩家升级时
	'''
	for obj in gActivityList.itervalues():
		if hasattr(obj, "onUpLevel"):
			obj.onUpLevel(who)
			
def onLogin(who, bRelogin):
	'''玩家登录时
	'''
	for obj in gActivityList.itervalues():
		if hasattr(obj, "onLogin"):
			obj.onLogin(who, bRelogin)

def onOffline(who):
	'''玩家离线时
	'''
	for obj in gActivityList.itervalues():
		if hasattr(obj, "onOffline"):
			obj.onOffline(who)

import productKeeper
import factoryConcrete

if "gActivityKeeper" not in globals():
	gActivityKeeper = productKeeper.cProductkeeper(factoryConcrete.activityFtr)
	gActivityList = {}

from common import *
import activity.load
import factory
import timerEvent