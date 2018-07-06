# -*- coding: utf-8 -*-
'''幻波池
'''


MAGIC_WAVE_TASK_PARENT_ID = 30501

def giveMagicWaveTask(who):
	'''获得任务30501
	'''
	if task.hasTask(who, MAGIC_WAVE_TASK_PARENT_ID):
		return
	taskObj = task.newTask(who, None, MAGIC_WAVE_TASK_PARENT_ID)


import task


