# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·援军'''
	intro = '''终于脱险了，此时遇到$target与白谷逸御剑而来'''
	detail = '''终于脱险了，此时遇到$target与白谷逸御剑而来'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2043,NI2044,E(2043,2058),E(2044,2059)'''
#导表结束