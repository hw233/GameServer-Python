#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
def getEndPointByRoleId(iRoleId):
	return gRoleIdMapEndPoint.getProxy(iRoleId)

def getEndPointByUserSourceAccount(sUserSource,sAccount):
	return gAccountMapEndPoint.getProxy(sUserSource,sAccount)

import u
import misc
import keeper

class cProxyManager(misc.cEndPointProxyManager):
	def _getEndPoint(self,iEndPointId):#override
		return gEndPointKeeper.getObj(iEndPointId)

if 'gbOnce' not in globals():
	gbOnce=True

	if 'mainService' in SYS_ARGV:
		gEndPointKeeper=misc.cEndPointKeeper()#endPoint id 映射 endPoint
		gRoleIdMapEndPoint=cProxyManager()#角色id映射endPoint,value是proxy
		gAccountMapEndPoint=cProxyManager()#用户来源与账号映射endPoint,value是proxy
	
def getSceneEP():
	'''场景服
	'''
	return backEnd.gSceneEp4ms

def getChatEP():
	'''聊天服
	'''
	return backEnd.gChatEp4ms

def getFightEP():
	'''战斗服
	'''
	return backEnd.gFightEp4ms

import gevent.server

import c
import log
import timeU
import backEnd
