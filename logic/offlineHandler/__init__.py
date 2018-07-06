# -*- coding: utf-8 -*-
'''玩家离线处理
'''
import jitKeeper
import factoryConcrete
import factory

def getOffline(roleId):
	'''获取离线玩家对象
	'''
	offlineObj = gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, roleId)
	return offlineObj

def addHandler(roleId, handlerName, **kwargs):
	offlineObj = getOffline(roleId)
	if offlineObj:
		offlineObj.addHandler(handlerName, **kwargs)
	
def executeHandler(who):
	offlineObj = getOffline(who.id)
	if offlineObj:
		offlineObj.executeHandler(who)


if 'gKeeper' not in globals():
	gKeeper = jitKeeper.cJITproductKeeper(factoryConcrete.offlineFtr)