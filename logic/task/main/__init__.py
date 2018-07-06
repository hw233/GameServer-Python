# -*- coding: utf-8 -*-
'''主线
'''

def checkMainTask(who,npcObj=None):
	if who.level%10!=0:
		return
	taskObj = task.hasTask(who, 40001)
	if taskObj:
		if taskObj.id == 40000:
			task.removeTask(who,taskObj.id)
		else:
			return
	taskId = 40001 + who.level*10
	task.newTask(who, npcObj, taskId)
	

import task