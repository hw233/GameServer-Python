# -*- coding: utf-8 -*-

TIME_CHECK = 10 * 60 # 离线任务检查间隔
OFFLINE_TASK = 30101 # 离线任务id
TIME_OUT = 2 * 60 * 60  #超时间隔

def addOfflineRing(who):
	'''增加剩余离线任务次数
	'''
	who.day.add("offlineRing", 1)
	if getOfflineRing(who) < 1:
		task.offlineTask.quitOfflineTask(who)

def getOfflineRing(who):
	'''获取剩余离线任务次数
	'''
	taskObj = task.getTask(30101)
	ringMax = taskObj.getOfflineRing()
	ring = ringMax - who.day.fetch("offlineRing", 0)
	return max(0, ring)

def inOfflineTask(who):
	'''是否离线任务中
	'''
	if hasattr(who, "hasOfflineTask"):
		return True
	return False
	
def tryOfflineTask(who):
	'''尝试离线任务
	'''
	if checkStartTask(who):
		startTask(who)
		return True
	return False

def checkStartTask(who):
	'''检查是否开始离线任务
	'''
	if not who.isOfflineTask():
		return False
	if getOfflineRing(who) < 1:
		return False

	sceneObj = scene.getScene(who.sceneId)
	if sceneObj.denyTeam:
		return False
	if who.denyTeam:
		return False

	return True

def startTask(who):
	'''开始离线任务
	'''
	who.hasOfflineTask = True
	who.lastOfflineRing = getOfflineRing(who)
	who.startTimer(functor(checkTaskState, who.id), TIME_CHECK, "checkTaskState")
	
	teamObj = who.getTeamObj()
	if teamObj:
		if teamObj.isLeader(who.id):
			teamObj.remove(who.id)
		elif task.hasTask(who, OFFLINE_TASK):
			if teamObj.getState(who.id) == TEAM_STATE_LEAVE:
				teamObj.setBack(who)
			return
	
	autoMatchTaskTeam(who)
	
def checkTaskState(roleId):
	'''检查离线任务状态
	'''
	who = getRole(roleId)
	if not who:
		return
	
	if checkTimeOut(who):
		quitOfflineTask(who)
		return

	who.startTimer(functor(checkTaskState, who.id), TIME_CHECK, "checkTaskState")

	offlineRing = getOfflineRing(who)
	if who.lastOfflineRing == offlineRing:
		if not hasattr(who,"notInOfflineTaskTime"):
			who.notInOfflineTaskTime = getSecond()
		autoMatchTaskTeam(who)
	else:
		if hasattr(who,"notInOfflineTaskTime"):
			del who.notInOfflineTaskTime
		who.lastOfflineRing = offlineRing

def checkTimeOut(who):
	'''检查是否超时了
	'''
	if not hasattr(who,"notInOfflineTaskTime"):
		return False
	if getSecond() - who.notInOfflineTaskTime < TIME_OUT:
		return False
	return True

def autoMatchTaskTeam(who):
	'''自动匹配降魔队伍
	'''
	if who.inWar():
		who.addHandlerForWarEnd("autoMatchTaskTeam", autoMatchTaskTeam)
		return

	teamObj = who.getTeamObj()
	if teamObj:
		teamObj.remove(who.id)

	team.platformservice.offlineMatch(who)
	
def quitOfflineTask(who, kick=True):
	'''退出离线任务
	'''
	who.stopTimer("checkTaskState")
	who.setOfflineTask(False)
	team.platformservice.cancleOfflineMatch(who)
	if hasattr(who, "hasOfflineTask"):
		del who.hasOfflineTask
	if hasattr(who, "lastOfflineRing"):
		del who.lastOfflineRing

	if who.inWar():
		who.addHandlerForWarEnd("quitOfflineTask", functor(quitOfflineTask, kick))
		return
		
	teamObj = who.getTeamObj()
	if teamObj:
		teamObj.remove(who.id)
	
	if kick: # 踢下线
		role.removeRole(who.id)


from common import *
from team.defines import *
import team.platformservice
import role
import task
import scene