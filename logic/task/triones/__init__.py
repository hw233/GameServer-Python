# -*- coding: utf-8 -*-
'''北斗七星
'''

TRIONES_TASK_PARENT_ID = 20201

def giveTrionesTask(who):
	'''获得任务20201
	'''
	if task.hasTask(who, TRIONES_TASK_PARENT_ID):
		return
	taskObj = task.newTask(who, None, TRIONES_TASK_PARENT_ID)
	return taskObj

import task

