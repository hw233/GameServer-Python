# -*- coding: utf-8 -*-
'''师门任务
'''

def randSchoolTask(who, npcObj=None, lastRing=False):
	'''随机师门任务
	'''
	taskObj = task.getTask(30001)
	if not taskObj:
		raise Exception("随机师门任务：没有找到30001任务")
	
	#是否最后一轮任务
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
		npcObj = npc.defines.getSchoolMaster(who.school)
	return task.newTask(who, npcObj, taskId)


def autoSchoolTask(who, npcObj=None):
	'''自动领取师门任务
	'''
	if task.hasTask(who, 30001):
		return
	if who.day.fetch("schoolRing") != 0:
		return
	if who.level == 20:
		task.newTask(who, npcObj, 30000)
		return
	task.school.randSchoolTask(who, npcObj)
	
	
	
from common import *
import task
import npc.defines
import findSort
import rand