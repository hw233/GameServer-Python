# -*- coding: utf-8 -*-
'''周答题-天问初试
'''


WEEKANSWER_TASK_PARENT_ID = 20001

def hasWeekAnswerTask(who):
	return task.hasTask(who, WEEKANSWER_TASK_PARENT_ID)

def giveWeekAnswerTask(who):
	'''获得任务20001
	'''
	if task.hasTask(who, WEEKANSWER_TASK_PARENT_ID):
		return False
	taskObj = task.newTask(who, None, WEEKANSWER_TASK_PARENT_ID)
	return True

import task

