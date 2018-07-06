# -*- coding: utf-8 -*-
if "gTaskList" not in globals():
	gTaskList = {}

def init():
	print "task init..."
	import task.load

def create(taskId):
	return task.load.getModule(taskId).Task(taskId)
	
def createAndLoad(pid, taskId, data):
	taskObj = create(taskId)
	taskObj.load(data)
	if not taskObj.isValid():
		return None
	return taskObj

def newTask(who, npcObj, taskId, **kwargs):
	'''新建任务
	'''
	if npcObj:
		npcObj = npcObj.this()
	taskObj = create(taskId)
	taskObj.onBorn(who, npcObj, **kwargs)
	if isinstance(taskObj, task.object.TeamTask):
		teamObj = who.getTeamObj()
		teamObj.addTask(taskObj)
		writeLog("task/new", "%d %s%s new task %d" % (who.id, teamObj.id, taskObj.roleList, taskId))
	else:
		who.addTask(taskObj)
		writeLog("task/new", "%d new task %d" % (who.id, taskId))
	return taskObj

def removeTask(who, taskId):
	'''移除任务
	'''
	taskObj = who.taskCtn.getItem(taskId)
	if taskObj:
		writeLog("task/remove", "%d remove task %d" % (who.id, taskId))
		who.removeTask(taskObj)
	else:
		teamObj = who.getTeamObj()
		if teamObj:
			taskObj = teamObj.taskCtn.getItem(taskId)
			if taskObj:
				writeLog("task/remove", "%d %d%s remove task %d" % (who.id, teamObj.id, taskObj.roleList, taskId))
				who.getTeamObj().removeTask(taskObj)
	
def hasTask(who, taskId):
	'''是否有某类任务
	'''
	taskObj = getTask(taskId)
	parentId = taskObj.parentId

	for taskObj in who.taskCtn.getAllValues():
		if taskObj.parentId == parentId:
			return taskObj
	
	teamObj = who.getTeamObj()
	if teamObj:
		for taskObj in teamObj.taskCtn.getAllValues():
			if taskObj.parentId == parentId:
				return taskObj
	return None

def goAhead(roleId, taskId):
	'''前往
	'''
	who = getRole(roleId)
	if not who:
		return
	taskObj = task.hasTask(who,taskId)
	if taskObj:
		taskObj.goAhead(who)
		
def getTask(taskId):
	'''获取缓存中的任务
	'''
	global gTaskList
	if taskId not in gTaskList:
		taskObj = create(taskId)
		if taskObj:
			gTaskList[taskId] = taskObj
	
	return gTaskList.get(taskId)

def onNewDay(who):
	'''玩家刷天时
	'''
	#task.school.autoSchoolTask(who)
	# 10301旧任务
	# taskObj = task.hasTask(who, 10301)
	# if taskObj:
	# 	taskObj.onNewDay()
	taskObj = task.hasTask(who, 10001)
	if taskObj:
		taskObj.onNewDay()
	else:
		task.holiday.autoHolidayTask(who)

def onUpLevel(who):
	'''玩家升级时
	'''
	# try:
	# 	task.main.checkMainTask(who)
	# except Exception:
	# 	logException()
	# if who.level == 20:
	# 	task.school.autoSchoolTask(who)
	task.pett.autoPetTask(who)
	task.holiday.autoHolidayTask(who)
	# if who.level == 15:
	# 	task.map.autoMapTask(who)
	pass

def onLogin(who, reLogin):
	'''玩家登录时
	'''
	task.holiday.autoHolidayTask(who)
	#task.school.autoSchoolTask(who)
	
	taskList = []
	for taskObj in who.taskCtn.getAllValues():
		taskList.append(taskObj)
		
	teamObj = who.inTeam()
	if teamObj:
		for taskObj in teamObj.taskCtn.getAllValues():
			taskList.append(taskObj)

	for taskObj in taskList:
		if hasattr(taskObj, "onLogin"):
			taskObj.onLogin(who, reLogin)


from common import *
import task.load
import task.object
import task.main
import task.school
import task.pett
import task.offlineTask
import task.holiday