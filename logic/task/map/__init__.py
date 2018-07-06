# -*- coding: utf-8 -*-
'''宝图任务
'''

TASK_MAP_PARENT_ID = 50201

def autoMapTask(who, npcObj=None):
	if task.hasTask(who, TASK_MAP_PARENT_ID):
		return
	if who.level == 15:
		task.newTask(who, npcObj, 50200)


import task
