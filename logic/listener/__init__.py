# -*- coding: utf-8 -*-
'''监听系统
'''

def init():
	print "listener init"
	global gListenerList
	gListenerList = {}
	for listenerId, mod in listener.load.moduleList.iteritems():
		listenerObj = mod.Listener(listenerId)
		for eventType in listenerObj.eventTypeList:
			if eventType not in gListenerList:
				gListenerList[eventType] = {}
			gListenerList[eventType][listenerId] = listenerObj

def doListen(eventType, roleId, **kwargs):
	'''监听
	'''
	if isinstance(roleId, (int, long)):
		roleId = roleId
	else:
		who = roleId
		roleId = who.id
	gevent.spawn(_doListen, eventType, roleId, **kwargs)
	
def _doListen(eventType, roleId, **kwargs):
	who = getRole(roleId)
	if not who:
		return
	
	listenerList = gListenerList.get(eventType)
	if not listenerList:
		return
	
	for listenerObj in listenerList.itervalues():
		if not listenerObj.checkCondition(who, **kwargs):
			continue
		listenerObj.triggerEvent(who, **kwargs)


from common import *
import gevent
import listener.load