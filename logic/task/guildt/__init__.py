# -*- coding: utf-8 -*-
'''帮派任务
'''

def randGuildTask(who, npcObj=None, lastRing=False):
	'''随机帮派任务
	'''
	taskObj = task.getTask(30201)
	if not taskObj:
		raise Exception("随机帮派任务：没有找到30201任务")
	if task.hasTask(who, 30201):
		return None
	# 是否最后一轮任务
	if lastRing:
		taskData = findSort.getRightValue(who.level, taskObj.lastRingTask)
	else:
		taskData = findSort.getRightValue(who.level, taskObj.ringTask)
	
	if not taskData:
		return None

	index = chooseKey(taskData, key="权重")
	taskId = taskData[index].get("编号", 0)
	if not taskId:
		return None
	if not npcObj:
		npcObj = who.getGuildObj().getNpcByType("总管")
	return task.newTask(who, npcObj, taskId)

def canTakeGuildTask(who):
	'''是否可以接取帮派任务
	'''
	maxCnt = getDatePart(partName="wday") * 20
	weekRing = who.week.fetch("guildRing")
	return weekRing < maxCnt


from common import *
import task
import npc.defines
import findSort
