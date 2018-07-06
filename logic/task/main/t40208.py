# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·灾祸'''
	intro = '''村门口突然来了一批妖物，速去抵抗'''
	detail = '''村门口突然来了一批妖物，速去抵抗'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1008,NI1009,NI1010,E(1008,1031),E(1009,1032),E(1010,1033)'''
#导表结束