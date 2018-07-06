# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·警讯'''
	intro = '''就在此时，$target匆匆忙忙赶来'''
	detail = '''就在此时，$target匆匆忙忙赶来'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2045,E(2045,2060)'''
#导表结束