# -*- coding: utf-8 -*-
'''宠物任务
'''


PET_TASK_LEAD_NO = 50000
PET_TASK_PARENTID = 50001

def getPetGroupTask():
	taskObj = task.getTask(task.pett.PET_TASK_PARENTID)
	if not taskObj:
		return
	groupTask = taskObj.groupTask
	lvKeys = groupTask.keys()
	lvKeys.sort()
	return lvKeys,groupTask

def autoPetTask(who, npcObj=None):
	'''自动领取宠物任务引导任务
	'''
	#return # 暂时屏蔽
	taskId = PET_TASK_LEAD_NO
	if task.hasTask(who, taskId):
		return

	taskId = PET_TASK_LEAD_NO
	if task.hasTask(who, PET_TASK_PARENTID):
		return

	taskObj = task.getTask(PET_TASK_PARENTID)
	groupTask = taskObj.groupTask
	# if who.level not in groupTask:
	# 	return

	lvKeys = groupTask.keys()
	lvKeys.sort()
	petComplete = who.taskCtn.fetch("petCom", {}) #{等级:[编号]}
	for lv in lvKeys:
		if lv > who.level:
			return
		#判断是否全部完成了
		completeTask = petComplete.get(lv, [])
		for info in groupTask[lv]:
			tasklist = info.get("任务",[])
			for no in tasklist:
				if no not in completeTask:
					task.newTask(who, npcObj, taskId)
					return
		
		
	
	
	
	
from common import *
import task
import npc.defines
