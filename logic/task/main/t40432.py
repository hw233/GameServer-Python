# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·心意'''
	intro = '''$target何去何从，问清楚他'''
	detail = '''$target何去何从，问清楚他'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2061,NI2062,E(2061,2082),E(2062,2083)'''
#导表结束