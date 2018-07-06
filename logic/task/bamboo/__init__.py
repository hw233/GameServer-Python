# -*- coding: utf-8 -*-
'''竹林除妖
'''

TASK_INSTANCE_PARENT_ID = 30401

def giveBambooTask(who):
	'''获得任务30401
	'''
	if task.hasTask(who, TASK_INSTANCE_PARENT_ID):
		return
	taskObj = task.newTask(who, None, TASK_INSTANCE_PARENT_ID)


import task
