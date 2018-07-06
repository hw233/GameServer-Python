# -*- coding: utf-8 -*-
'''入世修行
'''

def randRingTask(who, npcObj=None):
	'''随机任务
	'''
	taskObj = task.getTask(30601)
	if not taskObj:
		raise Exception("随机入世修行任务：没有找到30601任务")
	taskData = findSort.getRightValue(who.level, taskObj.ringTask)
	if not taskData:
		return None
	index = chooseKey(taskData, key="权重")
	taskId = taskData[index].get("编号", 0)
	if not taskId:
		return None
	return task.newTask(who, npcObj, taskId)

def answerRingHelped(who, targetRole, sResult):
	if not targetRole:
		return
	taskObj = task.getTask(30601)
	txt = taskObj.getText(4032, who.id)
	txt = txt.replace("$answer", sResult)
	message.tips(targetRole, txt)


from common import *
import task
import npc.defines
import findSort
import message
